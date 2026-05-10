#!/usr/bin/env python3
"""Resolve verbatim start/end cues to precise timestamps via YouTube auto-captions.

Usage:
  cue_to_timestamp.py <video_id> <start_cue> <end_cue> [near_sec]

Returns:
  START_TS=HH:MM:SS.mmm
  END_TS=HH:MM:SS.mmm
  DURATION=SS.mmm

Pads 0.3s on start and 0.5s on end to catch word edges. Caches .vtt at
~/ytclipper-fast/sources/<video_id>.en.vtt — fetches with yt-dlp on first call.
"""
import os, re, sys, subprocess

SOURCES = os.path.expanduser("~/ytclipper-fast/sources")
PAD_START = 0.3
PAD_END = 0.5


def ts_to_sec(s):
    h, m, rest = s.split(':')
    sec, ms = rest.split('.')
    return int(h)*3600 + int(m)*60 + int(sec) + int(ms)/1000


def sec_to_ts(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s - h*3600 - m*60
    return f"{h:02d}:{m:02d}:{sec:06.3f}"


def parse_vtt(path):
    cues = []
    with open(path) as f:
        content = f.read()
    for b in re.split(r'\n\n+', content):
        m = re.search(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', b)
        if not m:
            continue
        text = re.sub(r'<[^>]+>', '', b[m.end():]).strip()
        text = re.sub(r'align:\S+\s+position:\S+\s*', '', text)
        text = re.sub(r'\s+', ' ', text)
        if text:
            cues.append((ts_to_sec(m.group(1)), ts_to_sec(m.group(2)), text))
    return cues


_FILLER_RE = re.compile(r'\b(?:uh+|um+|er+|ah+|hm+|mhm+|you know|i mean|sort of|kind of|like)\b', re.IGNORECASE)


def norm(x):
    # Strip filler words first — auto-captions transcribe "uh"/"um" but operators
    # write cues without them. Both sides go through this filter so they line up.
    s = _FILLER_RE.sub(' ', x.lower())
    s = re.sub(r'[^\w\s]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def find_cue(cues, phrase, near_sec=None):
    target_words = norm(phrase).split()
    for n in range(min(len(target_words), 10), 2, -1):
        prefix = ' '.join(target_words[:n])
        hits = [(s, e, t) for s, e, t in cues if prefix in norm(t)]
        if hits:
            if near_sec is not None:
                hits.sort(key=lambda c: abs(c[0]-near_sec))
            return hits[0]
    return None


def ensure_vtt(video_id):
    path = os.path.join(SOURCES, f"{video_id}.en.vtt")
    if os.path.exists(path):
        return path
    os.makedirs(SOURCES, exist_ok=True)
    subprocess.run([
        "/opt/homebrew/bin/yt-dlp",
        "--write-auto-sub", "--sub-lang", "en",
        "--skip-download", "--sub-format", "vtt",
        f"https://www.youtube.com/watch?v={video_id}",
        "-o", os.path.join(SOURCES, f"{video_id}.%(ext)s"),
    ], check=True)
    return path


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    video_id = sys.argv[1]
    start_cue = sys.argv[2]
    end_cue = sys.argv[3]
    near = float(sys.argv[4]) if len(sys.argv) > 4 else None

    vtt = ensure_vtt(video_id)
    cues = parse_vtt(vtt)
    s = find_cue(cues, start_cue, near_sec=near)
    e = find_cue(cues, end_cue, near_sec=(near + 60) if near else None)
    if not s or not e:
        print(f"ERROR: start={s} end={e}", file=sys.stderr)
        sys.exit(2)

    start_ts = max(0, s[0] - PAD_START)
    end_ts = e[1] + PAD_END
    print(f"START_TS={sec_to_ts(start_ts)}")
    print(f"END_TS={sec_to_ts(end_ts)}")
    print(f"DURATION={end_ts - start_ts:.3f}")


if __name__ == "__main__":
    main()
