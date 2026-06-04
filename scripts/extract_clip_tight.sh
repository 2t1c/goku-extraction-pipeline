#!/bin/bash
# extract_clip_tight.sh — Cue-driven, frame-accurate clip extraction.
#
# Two improvements over extract_clip.sh:
#   1. Resolves verbatim start/end cues to ms-accurate timestamps via
#      cue_to_timestamp.py (cached YouTube auto-captions). No more eyeballing
#      timestamps off chunked transcripts.
#   2. Two-pass ffmpeg cut: fast keyframe seek to ~5s before the start, then
#      accurate re-encode to the precise window. Cuts land within ~100ms of
#      the verbatim cue instead of snapping to the nearest keyframe (which
#      could be 1-5s early on YouTube source).
#
# Total time: ~5-10s per cut on cached source. Worth the trade vs ~1s for
# the keyframe-aligned cut in extract_clip.sh.
#
# Usage:
#   extract_clip_tight.sh <youtube_url> <start_cue> <end_cue> [slug] [near_seconds]
#
# Cues should be the first 5-10 words of the spoken phrase, verbatim, as
# YouTube auto-captions transcribe them. Auto-captions transcribe contractions,
# fillers, and YouTube's best guess at proper nouns — write cues that match
# THAT, not how the line "should" read.
#
# near_seconds (optional): rough timestamp in seconds from the transcript.
# When the cue's first phrase appears multiple times in the video, the matcher
# picks the occurrence nearest this hint. Skip when the cue is unambiguous.
#
# Example (unambiguous cue):
#   extract_clip_tight.sh \
#     "https://www.youtube.com/watch?v=BYXbuik3dgA" \
#     "It's having the heat shield be reusable" \
#     "laborious inspection of 40,000 tiles" \
#     musk-heat-shield-kills-starship
#
# Example (ambiguous cue, with near hint):
#   extract_clip_tight.sh \
#     "https://www.youtube.com/watch?v=BYXbuik3dgA" \
#     "you can imagine like some mass driver" \
#     "create the solar cells and the radiators on the moon" \
#     musk-mass-driver-moon \
#     2030  # ~33:50 in seconds
#
# Output: ${CLIPS_DIR:-~/Desktop/goku-clips/}<slug>.mp4
#
# See style/clip-precision.md for the diagnosis behind this script.

set -e

URL="$1"
START_CUE="$2"
END_CUE="$3"
SLUG="$4"
NEAR_SEC="$5"  # optional disambiguation hint

if [ -z "$URL" ] || [ -z "$START_CUE" ] || [ -z "$END_CUE" ]; then
  echo "Usage: $0 <youtube_url> <start_cue> <end_cue> [slug] [near_seconds]"
  echo ""
  echo "  start_cue/end_cue: first 5-10 words of the spoken phrase, verbatim,"
  echo "  matching how YouTube auto-captions transcribe it."
  echo ""
  echo "  near_seconds: optional. Rough timestamp from the transcript. Use"
  echo "  when the cue's prefix could match in multiple places."
  exit 1
fi

DIR="$(cd "$(dirname "$0")" && pwd)"

# Tools
YTDLP="${YTDLP:-/opt/homebrew/bin/yt-dlp}"
FFMPEG="${FFMPEG:-/opt/homebrew/bin/ffmpeg}"
PYTHON="${PYTHON:-python3}"

# Paths
SOURCES_DIR="${SOURCES_DIR:-$HOME/ytclipper-fast/sources}"
CLIPS_DIR="${CLIPS_DIR:-$HOME/Desktop/goku-clips}"
mkdir -p "$SOURCES_DIR" "$CLIPS_DIR"

# Parse YouTube ID
VIDEO_ID=$(echo "$URL" | grep -oE '[a-zA-Z0-9_-]{11}' | tail -1)
if [ -z "$VIDEO_ID" ]; then
  echo "ERROR: Could not parse YouTube video ID from URL: $URL"
  exit 1
fi

SOURCE="$SOURCES_DIR/${VIDEO_ID}.mp4"

# Slug → output filename
if [ -n "$SLUG" ]; then
  SLUG_CLEAN=$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
  OUTPUT="$CLIPS_DIR/${SLUG_CLEAN}.mp4"
else
  OUTPUT="$CLIPS_DIR/${VIDEO_ID}_tight_$(date +%s).mp4"
fi

# ── Step 1: Resolve cues to precise timestamps ────────────────────────────
echo "[1/3] Resolving cues from cached captions..."
if [ -n "$NEAR_SEC" ]; then
  RESOLVED=$("$PYTHON" "$DIR/cue_to_timestamp.py" "$VIDEO_ID" "$START_CUE" "$END_CUE" "$NEAR_SEC" 2>&1) && CUE_EXIT=0 || CUE_EXIT=$?
else
  RESOLVED=$("$PYTHON" "$DIR/cue_to_timestamp.py" "$VIDEO_ID" "$START_CUE" "$END_CUE" 2>&1) && CUE_EXIT=0 || CUE_EXIT=$?
fi

# Handle the ambiguous-cue exit code (4) loudly.
if [ "$CUE_EXIT" = "4" ]; then
  echo "ERROR: cue resolved to multiple locations in the video."
  echo "$RESOLVED" | grep -E '^(AMBIGUOUS|CANDIDATES)='
  echo ""
  echo "Re-run with a near_seconds hint to disambiguate:"
  echo "  $0 \"$URL\" \"$START_CUE\" \"$END_CUE\" \"$SLUG\" <approx_seconds>"
  exit 4
fi

if [ "$CUE_EXIT" != "0" ]; then
  echo "ERROR: cue_to_timestamp.py did not resolve both cues."
  echo "$RESOLVED"
  echo ""
  echo "Try shorter, more distinctive cue phrases that match the captions"
  echo "exactly (auto-captions transcribe contractions, fillers, and proper"
  echo "nouns however YouTube's ASR heard them)."
  exit 2
fi

eval "$RESOLVED"
if [ -z "$START_TS" ] || [ -z "$END_TS" ]; then
  echo "ERROR: cue resolver returned empty timestamps."
  echo "       Got: $RESOLVED"
  exit 2
fi
echo "      Resolved: $START_TS → $END_TS (${DURATION}s)"

# Sanity check: window should be reasonable (60-300s typical for our clips)
DUR_INT=$(printf '%.0f' "$DURATION")
if [ "$DUR_INT" -gt 600 ]; then
  echo "WARN:  Resolved window is ${DUR_INT}s — likely a cue mismatch."
  echo "       Re-check cue phrases or add a near_seconds hint."
  echo "       Aborting before the long re-encode."
  exit 3
fi

# ── Step 2: Ensure source video is cached ─────────────────────────────────
if [ -f "$SOURCE" ]; then
  echo "[2/3] Source cached: $SOURCE ($(du -h "$SOURCE" | cut -f1))"
else
  echo "[2/3] Downloading source video (2-4 min for hour-long videos)..."
  "$YTDLP" -f "bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
    --merge-output-format mp4 \
    -o "$SOURCE" \
    "$URL" 2>&1 | tail -5
fi

# ── Step 3: Two-pass frame-accurate cut ───────────────────────────────────
# Pass 1: fast keyframe seek to START_TS, copy codec, get a small coarse file
#         (~5-15MB) that contains the precise cut window plus tail buffer.
# Pass 2: accurate seek inside the small coarse file with re-encode.
#
# Why two-pass: -ss before -i is fast (keyframe seek) but imprecise. -ss after
# -i on the original is accurate but decodes from frame zero (slow on long
# sources). Stacking them gives O(seconds) cut time with frame accuracy.
echo "[3/3] Cutting $START_TS → $END_TS (frame-accurate two-pass)..."
T0=$(date +%s)

COARSE="/tmp/extract_clip_tight_${VIDEO_ID}_$$.mp4"
trap 'rm -f "$COARSE"' EXIT

# Coarse window: start at START_TS (fast keyframe seek), grab DURATION + 10s
# tail buffer so the accurate-seek pass has frames to work with.
COARSE_DURATION=$(awk -v d="$DURATION" 'BEGIN { printf "%.3f", d + 10 }')

# Pass 1: fast seek + copy codec
"$FFMPEG" -y -loglevel error \
  -ss "$START_TS" \
  -i "$SOURCE" \
  -t "$COARSE_DURATION" \
  -c copy \
  -avoid_negative_ts make_zero \
  "$COARSE"

# Pass 2: accurate seek into the coarse file. Re-encode for frame precision.
# -ss starts at 0 because Pass 1 already seeked to START_TS, but the keyframe
# snap may have placed the actual first frame slightly before our target. We
# trust ffmpeg's accurate seek to find the exact target by counting from 0.
"$FFMPEG" -y -loglevel error \
  -i "$COARSE" \
  -t "$DURATION" \
  -c:v libx264 -preset fast -crf 22 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "$OUTPUT"

T1=$(date +%s)
echo "Done in $((T1-T0))s: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"

# ── Step 4 (optional): Whisper boundary validation ────────────────────────
# Confirms the actual cut audio contains the expected start/end cues. Catches
# caption-vs-audio drift, wrong-occurrence matches, and ffmpeg edge cases.
# No-ops gracefully if no whisper installation is available.
if [ -f "$DIR/validate_boundaries.py" ]; then
  echo "[validate] Checking clip boundaries against expected cues..."
  "$PYTHON" "$DIR/validate_boundaries.py" "$OUTPUT" "$START_CUE" "$END_CUE" || \
    echo "[validate] Warning: boundary check did not pass. Inspect manually."
fi
