#!/bin/bash
# caption_clip.sh — Burn captions into a clip in-place.
#
# Usage:
#   caption_clip.sh <clip_path> <video_id> <clip_start_HH:MM:SS>
#
# Behavior:
#   1. If ~/ytclipper-fast/transcripts/<video_id>.srt exists → slice it by
#      [start, start + clip_duration] and burn (~3-5s total).
#   2. Otherwise → run whisper.cpp directly on the clip (~15-20s total).
#   3. Atomically replace <clip_path> with the captioned version.
#
# Style (canonical, see style/clip-captioning.md):
#   Helvetica 24pt bold, white text, 1.5px black outline + 1.5px soft black
#   shadow, bottom-centered, 50px MarginV.

set -euo pipefail

CLIP="${1:?usage: caption_clip.sh <clip_path> <video_id> <clip_start_HH:MM:SS>}"
VIDEO_ID="${2:?usage: caption_clip.sh <clip_path> <video_id> <clip_start_HH:MM:SS>}"
CLIP_START="${3:?usage: caption_clip.sh <clip_path> <video_id> <clip_start_HH:MM:SS>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

WHISPER_BIN="${WHISPER_BIN:-$HOME/Desktop/AI Agents/remotion-captions/whisper.cpp/main}"
WHISPER_MODEL="${WHISPER_MODEL:-$HOME/Desktop/AI Agents/remotion-captions/whisper.cpp/models/ggml-small.en.bin}"
FFMPEG_FULL="${FFMPEG_FULL:-$HOME/Desktop/AI Agents/remotion-captions/ffmpeg-full}"
TRANSCRIPTS_DIR="${TRANSCRIPTS_DIR:-$HOME/ytclipper-fast/transcripts}"

CACHED_SRT="$TRANSCRIPTS_DIR/${VIDEO_ID}.srt"
LOCK="$TRANSCRIPTS_DIR/${VIDEO_ID}.lock"

if [[ ! -f "$CLIP" ]]; then
  echo "[caption] ERROR: clip not found: $CLIP" >&2; exit 1
fi
if [[ ! -x "$FFMPEG_FULL" ]]; then
  echo "[caption] ERROR: ffmpeg-full missing/not executable: $FFMPEG_FULL" >&2; exit 1
fi

# Convert HH:MM:SS (or MM:SS) to seconds for SRT slicing
hms_to_s() {
  local t="$1"
  awk -F: '{ n=NF; s=0; m=1; for (i=n; i>=1; i--) { s += $i * m; m *= 60 } print s }' <<< "$t"
}
CLIP_START_S=$(hms_to_s "$CLIP_START")

# Duration of the clip in seconds (float). ffmpeg -i exits non-zero with no output target,
# so isolate it from pipefail with `|| true` in a subshell.
CLIP_DUR_S=$({ "$FFMPEG_FULL" -i "$CLIP" 2>&1 || true; } \
  | awk '/Duration:/ { gsub(",", "", $2); split($2,a,":"); print a[1]*3600 + a[2]*60 + a[3] }')
if [[ -z "$CLIP_DUR_S" ]]; then
  echo "[caption] ERROR: could not read clip duration from $CLIP" >&2
  exit 1
fi
CLIP_END_S=$(awk -v a="$CLIP_START_S" -v b="$CLIP_DUR_S" 'BEGIN { print a + b }')

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
WORK_SRT="$TMP/captions.srt"

t0=$(date +%s)

# Caption display granularity: --max-len 30 chars + --split-on-word gives ~4-6 word phrase chunks
# per cue. Sentence-level cues display too much text per frame for mobile-feed reading speed.
if [[ ! -x "$WHISPER_BIN" ]] || [[ ! -f "$WHISPER_MODEL" ]]; then
  echo "[caption] ERROR: whisper.cpp not configured. Set WHISPER_BIN and WHISPER_MODEL or install at $HOME/Desktop/AI Agents/remotion-captions/whisper.cpp/" >&2
  exit 1
fi
echo "[caption] running whisper on clip directly (phrase chunks)"
"$FFMPEG_FULL" -y -loglevel error -i "$CLIP" -ar 16000 -ac 1 -c:a pcm_s16le "$TMP/audio.wav"
"$WHISPER_BIN" -m "$WHISPER_MODEL" -f "$TMP/audio.wav" -osrt --max-len 30 --split-on-word -of "$TMP/captions" > "$TMP/whisper.log" 2>&1

echo "[caption] burning captions (libass) → in-place replace"
"$FFMPEG_FULL" -y -loglevel error -i "$CLIP" \
  -vf "subtitles=$WORK_SRT:force_style='Fontname=Avenir Next,Fontsize=24,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H80000000,BorderStyle=1,Outline=1.5,Shadow=1.5,Alignment=2,MarginV=50'" \
  -c:v libx264 -preset veryfast -crf 20 \
  -c:a copy \
  "$TMP/out.mp4"

mv "$TMP/out.mp4" "$CLIP"
t1=$(date +%s)
echo "[caption] done in $((t1 - t0))s → $CLIP"
