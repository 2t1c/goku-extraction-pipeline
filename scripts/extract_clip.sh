#!/bin/bash
# extract_clip.sh — Fast keyframe-seek clip extraction.
#
# Usage:
#   extract_clip.sh <youtube_url> <start HH:MM:SS> <end HH:MM:SS> [slug]
#
#   <slug> is optional. When provided, the output file is named "<slug>.mp4"
#   (lowercase, hyphens). When omitted, falls back to "<VIDEO_ID>_<START>_<END>.mp4".
#
#   Slug should match the Notion title and Typefully draft title for consistency
#   so files are easy to find in Finder. Example:
#     extract_clip.sh URL 00:34:09 00:36:42 andreessen-ovitz-7am-meeting
#
# Output: $CLIPS_DIR (default ~/Desktop/AI Agents/clips/)
#
# Performance lessons:
#   1. -ss BEFORE -i = keyframe seek (~1s). -ss after = decode-and-discard (~3-5min for far seeks).
#   2. -c copy = no re-encode. Source is already H.264/AAC; we just slice. ~1s instead of 30s+.
#   3. Source video is cached in ~/ytclipper-fast/sources/ across sessions. /tmp/ and temp/ get cleaned.

set -e

URL="$1"
START="$2"
END="$3"
SLUG="$4"  # optional descriptive filename (lowercase, hyphens)

if [ -z "$URL" ] || [ -z "$START" ] || [ -z "$END" ]; then
  echo "Usage: $0 <youtube_url> <start HH:MM:SS> <end HH:MM:SS> [slug]"
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

mkdir -p "$SOURCES_DIR" "$CLIPS_DIR"

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
  OUTPUT="$CLIPS_DIR/${SLUG_CLEAN}.mp4"
else
  # Fallback: VIDEO_ID + timestamps
  START_SAFE=$(echo "$START" | tr ':' '-')
  END_SAFE=$(echo "$END" | tr ':' '-')
  OUTPUT="$CLIPS_DIR/${VIDEO_ID}_${START_SAFE}_${END_SAFE}.mp4"
fi

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
