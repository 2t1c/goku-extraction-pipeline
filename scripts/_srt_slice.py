"""Slice an SRT file by [start_s, end_s] and re-offset to start at 0.

Usage:  python3 _srt_slice.py <src.srt> <out.srt> <clip_start_s> <clip_end_s>
"""

import re
import sys


def to_seconds(stamp: str) -> float:
    h, m, rest = stamp.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def from_seconds(t: float) -> str:
    if t < 0:
        t = 0.0
    h = int(t // 3600)
    t -= h * 3600
    m = int(t // 60)
    t -= m * 60
    s = int(t)
    ms = int(round((t - s) * 1000))
    if ms == 1000:
        ms = 0
        s += 1
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main() -> int:
    src, out, start_s, end_s = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])

    with open(src, encoding="utf-8") as f:
        text = f.read()

    cues_out = []
    idx = 1
    for block in re.split(r"\n\n+", text.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        # lines[0] is the cue index (whisper output), lines[1] is times, rest is text
        try:
            t_start_str, t_end_str = lines[1].split(" --> ")
        except ValueError:
            continue
        t_start = to_seconds(t_start_str)
        t_end = to_seconds(t_end_str)

        # Skip cues entirely outside the clip window
        if t_end <= start_s or t_start >= end_s:
            continue

        new_start = max(t_start, start_s) - start_s
        new_end = min(t_end, end_s) - start_s
        if new_end <= new_start:
            continue

        body = "\n".join(lines[2:]).strip()
        if not body:
            continue

        cues_out.append(
            f"{idx}\n{from_seconds(new_start)} --> {from_seconds(new_end)}\n{body}"
        )
        idx += 1

    with open(out, "w", encoding="utf-8") as f:
        f.write("\n\n".join(cues_out))
        if cues_out:
            f.write("\n")

    print(f"[srt_slice] wrote {idx - 1} cues to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
