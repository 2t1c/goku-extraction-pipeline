#!/bin/bash
# extract_clip.sh — Fast keyframe-seek clip extraction with auto-foldering by source.
#
# Usage:
#   extract_clip.sh <youtube_url> <start HH:MM:SS> <end HH:MM:SS> [slug] [source_folder]
#
#   <slug> is optional. When provided, the output file is named "<slug>.mp4"
#   (lowercase, hyphens). When omitted, falls back to "<VIDEO_ID>_<START>_<END>.mp4".
#
#   <source_folder> is optional. When provided, the clip lands in
#   "$CLIPS_DIR/<source_folder>/<slug>.mp4" — keeps clips grouped per parent
#   podcast/video for easy Finder browsing.
#
#   When <source_folder> is omitted, the script auto-derives it from the first
#   segment of <slug> (everything before the first hyphen). So:
#     - "baszucki-roblox-10m-vs-improbable" → folder "baszucki/"
#     - "andreessen-ovitz-7am-meeting"      → folder "andreessen/"
#     - "naval-no-calendar-friend"          → folder "naval/"
#
#   Slug should match the Notion sub-item title and Typefully draft title for
#   consistency. Examples:
#     extract_clip.sh URL 00:34:09 00:36:42 andreessen-ovitz-7am-meeting
#     extract_clip.sh URL 00:34:09 00:36:42 andreessen-ovitz-7am-meeting andreessen
#
# Output: $CLIPS_DIR/<source_folder>/<slug>.mp4
#         default $CLIPS_DIR is ~/Desktop/AI Agents/clips/
#
# Performance lessons:
#   1. -ss BEFORE -i = keyframe seek (~1s). -ss after = decode-and-discard (~3-5min for far seeks).
#   2. -c copy = no re-encode. Source is already H.264/AAC; we just slice. ~1s instead of 30s+.
#   3. Source video is cached in ~/ytclipper-fast/sources/ across sessions. /tmp/ and temp/ get cleaned.

set -e

URL="$1"
START="$2"
END="$3"
SLUG="$4"           # optional descriptive filename (lowercase, hyphens)
SOURCE_FOLDER="$5"  # optional subfolder; auto-derived from slug prefix if omitted

if [ -z "$URL" ] || [ -z "$START" ] || [ -z "$END" ]; then
  echo "Usage: $0 <youtube_url> <start HH:MM:SS> <end HH:MM:SS> [slug] [source_folder]"
  exit 1
fi

# Tools
YTDLP="${YTDLP:-/opt/homebrew/bin/yt-dlp}"
FFMPEG="${FFMPEG:-/opt/homebrew/bin/ffmpeg}"

# Source videos are large (500–1500 MB). Cached deeper in $HOME so they don't clutter visible folders.
SOURCES_DIR="${SOURCES_DIR:-$HOME/ytclipper-fast/sources}"

# Clips are user-facing — they get drag-dropped into Typefully manually.
# Default to a place visible in Finder, near the user's working folder.
CLIPS_DIR="${CLIPS_DIR:-$HOME/Desktop/AI Agents/clips}"

# Parse YouTube ID from URL (11-char alphanumeric/dash/underscore)
VIDEO_ID=$(echo "$URL" | grep -oE '[a-zA-Z0-9_-]{11}' | tail -1)
if [ -z "$VIDEO_ID" ]; then
  echo "ERROR: Could not parse YouTube video ID from URL: $URL"
  exit 1
fi

SOURCE="$SOURCES_DIR/${VIDEO_ID}.mp4"

if [ -n "$SLUG" ]; then
  # User-provided slug — sanitize: lowercase, replace whitespace + special chars with hyphens, strip leading/trailing
  SLUG_CLEAN=$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')

  # Resolve source folder: explicit arg → use as-is; otherwise derive from slug's first segment
  if [ -z "$SOURCE_FOLDER" ]; then
    SOURCE_FOLDER=$(echo "$SLUG_CLEAN" | cut -d'-' -f1)
  fi
  SOURCE_FOLDER_CLEAN=$(echo "$SOURCE_FOLDER" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')

  OUTPUT_DIR="$CLIPS_DIR/$SOURCE_FOLDER_CLEAN"
  OUTPUT="$OUTPUT_DIR/${SLUG_CLEAN}.mp4"
else
  # Fallback: VIDEO_ID + timestamps, flat in CLIPS_DIR (legacy behavior)
  START_SAFE=$(echo "$START" | tr ':' '-')
  END_SAFE=$(echo "$END" | tr ':' '-')
  OUTPUT_DIR="$CLIPS_DIR"
  OUTPUT="$OUTPUT_DIR/${VIDEO_ID}_${START_SAFE}_${END_SAFE}.mp4"
fi

mkdir -p "$SOURCES_DIR" "$OUTPUT_DIR"

# Step 1: Download source if not cached
if [ -f "$SOURCE" ]; then
  echo "[1/2] Source cached: $SOURCE ($(du -h "$SOURCE" | cut -f1))"
else
  echo "[1/2] Downloading source video (this may take 2–4 min for hour-long videos)..."
  "$YTDLP" -f "bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
    --merge-output-format mp4 \
    -o "$SOURCE" \
    "$URL" 2>&1 | tail -5
fi

# Step 1.5: Kick off background transcribe of full source (idempotent, no-op if cached or already running).
# This pre-warms ~/ytclipper-fast/transcripts/<VIDEO_ID>.srt so per-clip captioning becomes a 3-5s
# SRT slice + ffmpeg burn-in instead of a 15-20s whisper-on-clip run. See style/clip-captioning.md.
TRANSCRIBE_SCRIPT="$(dirname "$0")/transcribe_source.sh"
if [ -x "$TRANSCRIBE_SCRIPT" ]; then
  nohup bash "$TRANSCRIBE_SCRIPT" "$VIDEO_ID" > /tmp/transcribe-${VIDEO_ID}.log 2>&1 &
  disown || true
fi

# Step 2: Cut clip — fast keyframe seek + codec copy
echo "[2/2] Cutting $START → $END..."
T0=$(date +%s)
"$FFMPEG" -y -loglevel error \
  -ss "$START" -to "$END" \
  -i "$SOURCE" \
  -c copy \
  -avoid_negative_ts make_zero \
  "$OUTPUT" 2>&1
T1=$(date +%s)

echo "Done in $((T1-T0))s: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
