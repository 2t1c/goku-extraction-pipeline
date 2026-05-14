#!/usr/bin/env python3
"""Resolve verbatim start/end cues to precise timestamps via YouTube auto-captions.

Word-stream matcher: parses inline word-level timestamps from the .vtt
(format: `<00:33:53.840><c> word</c>`) into a flat (timestamp, word) stream,
then matches each cue against that stream with filler tolerance and gap
allowance. Handles auto-caption quirks the old caption-block matcher missed:

- Fillers inserted mid-cue ("It's uh having the heat shield...")
- Sentence-fragment splits across multiple caption blocks
- 1-2 mistranscribed words out of a 6-8 word cue

Usage:
  cue_to_timestamp.py <video_id> <start_cue> <end_cue> [near_sec]

Returns on stdout (eval-friendly):
  START_TS=HH:MM:SS.mmm
  END_TS=HH:MM:SS.mmm
  DURATION=SS.mmm

Or on ambiguity (multiple equally-good matches with no near_sec hint):
  AMBIGUOUS=start
  CANDIDATES=HH:MM:SS,HH:MM:SS,...
  (exit code 4)

Caches .vtt at ~/ytclipper-fast/sources/<video_id>.en.vtt — fetches with
yt-dlp on first call. Pads 0.3s on start and 0.5s on end to catch word edges.
"""
import os
import re
import sys
import subprocess

SOURCES = os.path.expanduser("~/ytclipper-fast/sources")
TRANSCRIPTS = os.path.expanduser("~/ytclipper-fast/transcripts")

# YouTube VTT auto-captions are timed loosely — pad generously.
PAD_START = 0.3
PAD_END = 0.5

# Whisper word-level SRT timestamps land within ~50ms of actual word onset.
# Tighten the padding accordingly so cuts open right on the syllable.
WHISPER_PAD_START = 0.05
WHISPER_PAD_END = 0.20

# Filler tokens that auto-captions transcribe but operators rarely write
# into cues. Stripped from BOTH cue and stream before matching.
_FILLER_RE = re.compile(
    r"\b(?:uh+|um+|er+|ah+|hm+|mhm+|you know|i mean|sort of|kind of|like)\b",
    re.IGNORECASE,
)


def ts_to_sec(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(".")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def sec_to_ts(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}"


def norm(x):
    """Lowercase, drop punctuation in-place, strip filler words, collapse whitespace.

    In-place punctuation removal (no space substitution) so things like
    "40,000" → "40000" and "I'm" → "im" — matching how YouTube auto-captions
    tend to emit numbers and contractions as single tokens.
    """
    s = _FILLER_RE.sub(" ", x.lower())
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _strip_word(w):
    """Lowercase, strip punctuation, return empty string if word is junk."""
    return re.sub(r"[^\w]", "", w.lower())


def parse_vtt_words(path):
    """Build a (start_sec, word) stream from a YouTube auto-generated VTT.

    YouTube's auto-VTT mixes two kinds of word emissions per "reveal" block:
      1. Inline-timestamped words: `<HH:MM:SS.sss><c> word</c>` — frame-accurate.
      2. Leading text: bare words at the start of the block body, no inline
         timestamp, contextually owned by the cue's start time.

    Each reveal block's leading text is a REPEAT of the previous block's body
    (with maybe 1-2 new words appended). Static blocks (cue_end ≈ cue_start)
    are duplicates and dropped. To get every word exactly once we:

      - Skip static blocks
      - Emit every inline-timestamped word at its precise time
      - Emit a leading-text word ONLY if no nearby (±5s) prior emission of the
        same word exists. That captures genuinely new leading words ("It's",
        "reusable") while suppressing the rolling-caption repeat.

    Words are lowercased and punctuation-stripped at parse time.
    """
    with open(path) as f:
        content = f.read()

    cue_re = re.compile(
        r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})[^\n]*\n(.+?)(?=\n\n|\Z)",
        re.DOTALL,
    )
    inline_word_re = re.compile(
        r"<(\d{2}:\d{2}:\d{2}\.\d{3})><c>\s*([^<]+?)\s*</c>"
    )
    first_ts_re = re.compile(r"<\d{2}:\d{2}:\d{2}\.\d{3}>")

    words = []
    # word → sorted list of timestamps already emitted, for ±5s dedup of leading text
    seen_times = {}
    LEAD_DEDUP_WINDOW = 5.0  # seconds

    def already_seen_near(word, ts, window):
        for prev in seen_times.get(word, ()):
            if abs(prev - ts) < window:
                return True
        return False

    def remember(word, ts):
        seen_times.setdefault(word, []).append(ts)

    for m in cue_re.finditer(content):
        cue_start = ts_to_sec(m.group(1))
        cue_end = ts_to_sec(m.group(2))
        body = m.group(3)

        # Static block (~10ms duration) is a duplicate of the previous reveal
        if cue_end - cue_start < 0.1:
            continue

        # Strip alignment attrs and HTML entities
        body = re.sub(r"align:\S+\s+position:\S+\s*", " ", body)

        # Split body into leading text and inline-timestamped portion
        first_inline = first_ts_re.search(body)
        if first_inline:
            leading = body[: first_inline.start()]
            inline_part = body[first_inline.start():]
        else:
            leading = body
            inline_part = ""

        # Leading text: emit each word only if no recent same-word emission
        for w in leading.split():
            stripped = _strip_word(w)
            if not stripped:
                continue
            if already_seen_near(stripped, cue_start, LEAD_DEDUP_WINDOW):
                continue
            words.append((cue_start, stripped))
            remember(stripped, cue_start)

        # Inline-timestamped words: always emit (each carries a unique ts)
        for wm in inline_word_re.finditer(inline_part):
            ts = ts_to_sec(wm.group(1))
            for w in wm.group(2).split():
                stripped = _strip_word(w)
                if not stripped:
                    continue
                # Suppress same-word-same-timestamp duplicates from rolling caption overlap
                if already_seen_near(stripped, ts, 0.05):
                    continue
                words.append((ts, stripped))
                remember(stripped, ts)

    words.sort(key=lambda x: x[0])
    return words


_SRT_CUE_RE = re.compile(
    r"\d+\s*\n"
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+"
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})[^\n]*\n"
    r"(.+?)(?=\n\s*\n|\Z)",
    re.DOTALL,
)


def parse_whisper_words_srt(path):
    """Parse a whisper.cpp word-level SRT (produced with --max-len 1 --split-on-word)
    into the same (start_sec, word) stream format as parse_vtt_words.

    Each SRT cue is typically a single token with millisecond-precise start/end.
    Tokens that normalize to empty (punctuation-only) are skipped.
    """
    with open(path, encoding="utf-8") as f:
        content = f.read()

    words = []
    for m in _SRT_CUE_RE.finditer(content):
        sh, sm, ss, sms = (int(m.group(i)) for i in range(1, 5))
        start_sec = sh * 3600 + sm * 60 + ss + sms / 1000.0
        text = m.group(9)
        # whisper splits multi-word tokens like "I'm" → "I" + "m" but also emits
        # composite cues occasionally — handle both.
        for w in text.split():
            stripped = _strip_word(w)
            if not stripped:
                continue
            words.append((start_sec, stripped))

    words.sort(key=lambda x: x[0])
    return words


def find_cue(words, cue, near_sec=None, return_all=False):
    """Locate the cue in the word stream.

    Returns (start_sec, end_sec) for the best match, OR a list of
    (start_sec, end_sec) candidates when multiple matches are ambiguous.
    """
    # Tokenize the cue with the same filter as the stream.
    cue_tokens = norm(cue).split()
    if len(cue_tokens) < 3:
        return None
    n_cue = len(cue_tokens)

    # We use up to the first 8 cue tokens as the matcher target.
    # Allows >8-word cues but only the leading window has to match.
    target = cue_tokens[: min(8, n_cue)]
    n_target = len(target)
    # Allow window up to 2× the target length to absorb in-stream fillers
    # (already partially stripped) and non-cue interjections.
    window_size = n_target * 2

    # Pre-filter the word stream: drop tokens that normalize to nothing
    # (fillers, punctuation-only). Keep timestamps aligned.
    clean = [(ts, w) for ts, w in words if norm(w)]

    candidates = []  # (start_ts, end_ts, score, hit_ratio)

    for i in range(len(clean) - n_target + 1):
        if clean[i][1] != target[0]:
            continue
        # Try to consume the rest of `target` within `window_size` positions.
        # At each window step, allow skipping up to 2 target tokens — handles
        # caption-vs-cue mismatches like "one" vs "1", "gigabytes" vs "gb".
        # Skipped tokens count as "missed" against the threshold.
        j = 1  # next target index to match
        end_ts = clean[i][0]
        for k in range(1, min(window_size, len(clean) - i)):
            if j >= n_target:
                break
            sw = clean[i + k][1]
            for skip in range(min(3, n_target - j)):
                if sw == target[j + skip]:
                    end_ts = clean[i + k][0]
                    j += skip + 1
                    break
        # Accept if we matched ≥ (n_target - 2) tokens of n_target — allows
        # up to two mistranscribed/skipped tokens in an 8-word target window.
        threshold = max(3, n_target - 2)
        if j >= threshold:
            candidates.append((clean[i][0], end_ts, j / n_target))

    if not candidates:
        return None

    # Collapse near-duplicate candidates (within 3 sec of each other).
    candidates.sort()
    deduped = [candidates[0]]
    for c in candidates[1:]:
        if c[0] - deduped[-1][0] > 3:
            deduped.append(c)

    if near_sec is not None:
        deduped.sort(key=lambda c: abs(c[0] - near_sec))
        return deduped[0][:2]

    # Single high-confidence candidate → return it
    if len(deduped) == 1:
        return deduped[0][:2]

    # Multiple candidates — check if the top one matches more tokens than the
    # rest. If so, prefer it; otherwise return all and let caller decide.
    deduped.sort(key=lambda c: (-c[2], c[0]))
    if deduped[0][2] > deduped[1][2] + 0.15:
        return deduped[0][:2]

    if return_all:
        return [c[:2] for c in deduped[:5]]
    return [c[:2] for c in deduped[:5]]


def ensure_vtt(video_id):
    path = os.path.join(SOURCES, f"{video_id}.en.vtt")
    if os.path.exists(path):
        return path
    os.makedirs(SOURCES, exist_ok=True)
    subprocess.run(
        [
            "/opt/homebrew/bin/yt-dlp",
            "--write-auto-sub",
            "--sub-lang",
            "en",
            "--skip-download",
            "--sub-format",
            "vtt",
            f"https://www.youtube.com/watch?v={video_id}",
            "-o",
            os.path.join(SOURCES, f"{video_id}.%(ext)s"),
        ],
        check=True,
    )
    return path


def _suggest_nearest_phrase(words, cue, k=3):
    """Pick the k word-stream substrings whose token sequence most overlaps the
    cue tokens. Used to surface 'did you mean…' hints when a cue is not found.
    """
    cue_tokens = norm(cue).split()
    if not cue_tokens:
        return []
    n = len(cue_tokens)
    clean = [(ts, w) for ts, w in words if norm(w)]
    cue_set = set(cue_tokens)
    scored = []
    for i in range(0, len(clean) - n + 1):
        window = [clean[i + j][1] for j in range(n)]
        overlap = sum(1 for w in window if w in cue_set)
        if overlap >= max(2, n // 2):
            scored.append((overlap, clean[i][0], " ".join(window)))
    scored.sort(key=lambda x: (-x[0], x[1]))
    seen = []
    out = []
    for sc, ts, phrase in scored:
        if any(abs(ts - prev_ts) < 5 for prev_ts in seen):
            continue
        seen.append(ts)
        out.append((sec_to_ts(ts), phrase))
        if len(out) >= k:
            break
    return out


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    video_id = sys.argv[1]
    start_cue = sys.argv[2]
    end_cue = sys.argv[3]
    near = float(sys.argv[4]) if len(sys.argv) > 4 else None

    # Source priority: whisper word-level SRT > YouTube VTT auto-captions.
    # Whisper is ~10x more accurate on proper nouns and numbers, and its word
    # boundaries are ~50ms vs VTT's ~300ms. See style/clip-captioning.md.
    whisper_words = os.path.join(TRANSCRIPTS, f"{video_id}.words.srt")
    if os.path.exists(whisper_words):
        words = parse_whisper_words_srt(whisper_words)
        source = "whisper"
        pad_start, pad_end = WHISPER_PAD_START, WHISPER_PAD_END
        print(f"# source=whisper-words ({whisper_words})", file=sys.stderr)
    else:
        vtt = ensure_vtt(video_id)
        words = parse_vtt_words(vtt)
        source = "vtt"
        pad_start, pad_end = PAD_START, PAD_END
        print(f"# source=youtube-vtt ({vtt})", file=sys.stderr)

    # Resolve END cue first — usually more distinctive (specific final
    # phrases land uniquely). If unique, its timestamp anchors the START
    # cue search.
    end_match = find_cue(words, end_cue, near_sec=(near + 60) if near else None)
    if end_match is None:
        print(f"ERROR: end cue not found in {source} stream: {end_cue!r}", file=sys.stderr)
        suggestions = _suggest_nearest_phrase(words, end_cue)
        if suggestions:
            print("DID_YOU_MEAN=", file=sys.stderr)
            for ts, phrase in suggestions:
                print(f"  {ts}  '{phrase}'", file=sys.stderr)
        sys.exit(2)

    if isinstance(end_match, list):
        # End cue ambiguous. Without near hint we can't pick.
        if near is None:
            print(f"AMBIGUOUS=end", file=sys.stderr)
            print(
                "CANDIDATES=" + ",".join(sec_to_ts(c[0]) for c in end_match),
                file=sys.stderr,
            )
            sys.exit(4)
        end_match.sort(key=lambda c: abs(c[0] - (near + 60)))
        end_match = end_match[0]

    end_start_sec, end_end_sec = end_match
    end_ts = end_end_sec + pad_end

    # Use END cue location as anchor for START cue search if no operator hint.
    # Estimate start within ~5 minutes before end (typical clip ≤ 4 min).
    auto_near = end_start_sec - 90 if near is None else near

    start_match = find_cue(words, start_cue, near_sec=auto_near)
    if start_match is None:
        print(f"ERROR: start cue not found in {source} stream: {start_cue!r}", file=sys.stderr)
        suggestions = _suggest_nearest_phrase(words, start_cue)
        if suggestions:
            print("DID_YOU_MEAN=", file=sys.stderr)
            for ts, phrase in suggestions:
                print(f"  {ts}  '{phrase}'", file=sys.stderr)
        sys.exit(2)

    if isinstance(start_match, list):
        # Multiple candidates even with auto_near. If user passed an explicit
        # near hint we trust it; otherwise warn loudly and abort.
        start_match.sort(key=lambda c: abs(c[0] - auto_near))
        if near is not None:
            start_match = start_match[0]
        else:
            # Within 30 sec of auto_near → use it. Beyond that → ambiguous.
            best = start_match[0]
            if abs(best[0] - auto_near) <= 30:
                start_match = best
            else:
                print(f"AMBIGUOUS=start", file=sys.stderr)
                print(
                    "CANDIDATES="
                    + ",".join(sec_to_ts(c[0]) for c in start_match),
                    file=sys.stderr,
                )
                sys.exit(4)

    start_start_sec, _ = start_match
    start_ts = max(0, start_start_sec - pad_start)

    print(f"START_TS={sec_to_ts(start_ts)}")
    print(f"END_TS={sec_to_ts(end_ts)}")
    print(f"DURATION={end_ts - start_ts:.3f}")


if __name__ == "__main__":
    main()
