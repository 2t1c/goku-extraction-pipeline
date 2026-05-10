#!/usr/bin/env python3
"""Validate that a cut clip's first/last few seconds contain the expected cues.

Runs whisper on the boundary audio (not the whole clip — just the first 4s
and last 4s) and fuzzy-matches the transcribed words against the expected
cue text. Catches:

- Caption-vs-audio drift (rare but real, especially around silence)
- Wrong-occurrence matches the cue resolver couldn't disambiguate
- ffmpeg edge cases that produce a clip with the wrong start/end frames

Usage:
  validate_boundaries.py <clip.mp4> <start_cue> <end_cue>

Exit codes:
  0  → both boundaries contain the expected cues, OR whisper not available
  1  → at least one boundary failed (clip likely needs re-cut)

Whisper installations supported (auto-detected, in priority order):
  1. mlx_whisper (Python, Apple Silicon native, fastest on M-series)
  2. faster_whisper (Python, CPU/CUDA, cross-platform)
  3. whisper-cpp (binary, $(which whisper-cpp))

If none are available, prints a one-line note and exits 0 (graceful no-op).
Install one to enable validation:

  pip install mlx-whisper        # macOS Apple Silicon
  pip install faster-whisper     # cross-platform
  brew install whisper-cpp       # macOS Homebrew binary
"""
import os
import re
import subprocess
import sys
import tempfile

BOUNDARY_SECONDS = 4.0  # how much of each end to transcribe
MATCH_THRESHOLD = 0.5  # fraction of cue tokens that must appear in boundary

_FILLER_RE = re.compile(
    r"\b(?:uh+|um+|er+|ah+|hm+|mhm+|you know|i mean|sort of|kind of|like)\b",
    re.IGNORECASE,
)


def norm(x):
    s = _FILLER_RE.sub(" ", x.lower())
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def get_duration(path):
    out = subprocess.run(
        [
            "/opt/homebrew/bin/ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path,
        ],
        capture_output=True,
        text=True,
    )
    return float(out.stdout.strip())


def extract_boundary_audio(clip_path, kind, out_wav):
    """Extract WAV of either the first or last BOUNDARY_SECONDS of clip_path."""
    duration = get_duration(clip_path)
    if kind == "head":
        ss = "0"
        t = str(BOUNDARY_SECONDS)
    elif kind == "tail":
        ss = str(max(0, duration - BOUNDARY_SECONDS))
        t = str(BOUNDARY_SECONDS)
    else:
        raise ValueError(kind)

    subprocess.run(
        [
            "/opt/homebrew/bin/ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-ss",
            ss,
            "-t",
            t,
            "-i",
            clip_path,
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            out_wav,
        ],
        check=True,
    )


def transcribe_mlx(wav_path):
    import mlx_whisper  # noqa

    result = mlx_whisper.transcribe(wav_path, path_or_hf_repo="mlx-community/whisper-tiny")
    return result.get("text", "")


def transcribe_faster(wav_path):
    from faster_whisper import WhisperModel  # noqa

    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(wav_path, language="en")
    return " ".join(seg.text for seg in segments)


def transcribe_cpp(wav_path):
    out = subprocess.run(
        ["whisper-cpp", "-m", "tiny", "-l", "en", "-otxt", wav_path],
        capture_output=True,
        text=True,
    )
    return out.stdout


def get_transcriber():
    """Return a transcribe(wav_path) -> text function, or None."""
    try:
        import mlx_whisper  # noqa: F401

        return transcribe_mlx
    except ImportError:
        pass
    try:
        import faster_whisper  # noqa: F401

        return transcribe_faster
    except ImportError:
        pass
    if subprocess.run(["which", "whisper-cpp"], capture_output=True).returncode == 0:
        return transcribe_cpp
    return None


def cue_in_text(cue, text):
    """Return fraction of cue's first 6 tokens that appear in text, in order."""
    cue_tokens = norm(cue).split()[:6]
    text_tokens = norm(text).split()
    if not cue_tokens:
        return 0.0
    j = 0
    for t in text_tokens:
        if j < len(cue_tokens) and t == cue_tokens[j]:
            j += 1
    return j / len(cue_tokens)


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    clip = sys.argv[1]
    start_cue = sys.argv[2]
    end_cue = sys.argv[3]

    transcribe = get_transcriber()
    if transcribe is None:
        print(
            "[validate] No whisper installation found — skipping boundary check. "
            "Install with: pip install mlx-whisper",
        )
        sys.exit(0)

    failed = False
    with tempfile.TemporaryDirectory() as td:
        for kind, cue in [("head", start_cue), ("tail", end_cue)]:
            wav = os.path.join(td, f"{kind}.wav")
            extract_boundary_audio(clip, kind, wav)
            text = transcribe(wav)
            ratio = cue_in_text(cue, text)
            ok = ratio >= MATCH_THRESHOLD
            status = "OK" if ok else "FAIL"
            print(
                f"[validate] {kind:4s} ratio={ratio:.2f} {status}: "
                f"heard='{text.strip()[:80]}' expected='{cue[:60]}'"
            )
            if not ok:
                failed = True

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
