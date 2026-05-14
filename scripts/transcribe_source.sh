#!/bin/bash
# transcribe_source.sh — Transcribe a cached source video once and persist
# the SRT for cheap per-clip slicing later.
#
# Usage:  transcribe_source.sh <YOUTUBE_VIDEO_ID>
#
# Reads:  ~/ytclipper-fast/sources/<VIDEO_ID>.mp4
# Writes: ~/ytclipper-fast/transcripts/<VIDEO_ID>.srt
# Lock:   ~/ytclipper-fast/transcripts/<VIDEO_ID>.lock  (cleared on exit/crash)
#
# Idempotent — exits 0 if the SRT already exists.
# Safe to call in background:  bash transcribe_source.sh <id> &

set -euo pipefail

VIDEO_ID="${1:?usage: transcribe_source.sh <VIDEO_ID>}"

SOURCES_DIR="${SOURCES_DIR:-$HOME/ytclipper-fast/sources}"
TRANSCRIPTS_DIR="${TRANSCRIPTS_DIR:-$HOME/ytclipper-fast/transcripts}"
mkdir -p "$TRANSCRIPTS_DIR"

SOURCE_MP4="$SOURCES_DIR/${VIDEO_ID}.mp4"
SRT_OUT="$TRANSCRIPTS_DIR/${VIDEO_ID}.srt"            # sentence-level — used by caption_clip.sh
WORDS_SRT_OUT="$TRANSCRIPTS_DIR/${VIDEO_ID}.words.srt" # word-level — used by cue_to_timestamp.py
LOCK="$TRANSCRIPTS_DIR/${VIDEO_ID}.lock"

# Defaults point at the remotion-captions install. Override via env if you move them.
WHISPER_BIN="${WHISPER_BIN:-$HOME/Desktop/AI Agents/remotion-captions/whisper.cpp/main}"
WHISPER_MODEL="${WHISPER_MODEL:-$HOME/Desktop/AI Agents/remotion-captions/whisper.cpp/models/ggml-small.en.bin}"
FFMPEG_FULL="${FFMPEG_FULL:-$HOME/Desktop/AI Agents/remotion-captions/ffmpeg-full}"

if [[ -f "$SRT_OUT" && -f "$WORDS_SRT_OUT" ]]; then
  echo "[transcribe] cached: $SRT_OUT + $WORDS_SRT_OUT"
  exit 0
fi

if [[ -f "$LOCK" ]]; then
  echo "[transcribe] another run is already transcribing $VIDEO_ID (lock present)"
  exit 0
fi

if [[ ! -f "$SOURCE_MP4" ]]; then
  echo "[transcribe] ERROR: source not found: $SOURCE_MP4" >&2
  exit 1
fi
if [[ ! -x "$WHISPER_BIN" ]]; then
  echo "[transcribe] ERROR: whisper binary not executable: $WHISPER_BIN" >&2
  exit 1
fi
if [[ ! -f "$WHISPER_MODEL" ]]; then
  echo "[transcribe] ERROR: whisper model not found: $WHISPER_MODEL" >&2
  exit 1
fi
if [[ ! -x "$FFMPEG_FULL" ]]; then
  echo "[transcribe] ERROR: ffmpeg-full not executable: $FFMPEG_FULL" >&2
  exit 1
fi

# Drop lock and always clear it (even on crash)
echo "$$" > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"; rm -f "$LOCK"' EXIT

echo "[transcribe] extracting 16kHz mono WAV from $SOURCE_MP4"
"$FFMPEG_FULL" -y -loglevel error -i "$SOURCE_MP4" -ar 16000 -ac 1 -c:a pcm_s16le "$TMP/audio.wav"

if [[ ! -f "$SRT_OUT" ]]; then
  echo "[transcribe] pass 1/2 — sentence-level whisper.cpp small.en (3-5 min for 1hr audio)"
  "$WHISPER_BIN" \
    -m "$WHISPER_MODEL" \
    -f "$TMP/audio.wav" \
    -osrt \
    -of "$TMP/captions" \
    > "$TMP/whisper-sentence.log" 2>&1
  mv "$TMP/captions.srt" "$SRT_OUT"   # atomic move — partial files never look complete
  echo "[transcribe] pass 1/2 done: $SRT_OUT"
fi

if [[ ! -f "$WORDS_SRT_OUT" ]]; then
  echo "[transcribe] pass 2/2 — word-level whisper.cpp (--max-len 1 --split-on-word, for cue precision)"
  "$WHISPER_BIN" \
    -m "$WHISPER_MODEL" \
    -f "$TMP/audio.wav" \
    -osrt \
    --max-len 1 \
    --split-on-word \
    -of "$TMP/words" \
    > "$TMP/whisper-words.log" 2>&1
  mv "$TMP/words.srt" "$WORDS_SRT_OUT"
  echo "[transcribe] pass 2/2 done: $WORDS_SRT_OUT"
fi

echo "[transcribe] complete"
