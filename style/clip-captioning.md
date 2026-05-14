# Clip Captioning — burn captions into every clip before Notion

Every clip cut by the pipeline gets captions burned in **before** it lands in
Notion or Typefully. Captions are non-optional — X autoplays muted, and unmuted
viewing is the minority case.

## When this runs

Phase 2.3 of the extraction workflow — after `extract_clip.sh` writes the .mp4
to disk, before `notion_upload.py` uploads it. The captioned file overwrites
the original, so downstream upload steps need no changes.

```bash
bash scripts/caption_clip.sh <clip-path> <video-id> <clip-start-HH:MM:SS>
```

## Style spec (canonical)

Locked-in look matched to mobile-feed visibility on X:

| Property | Value |
|---|---|
| Font | Helvetica |
| Size | **24pt** (bold) |
| Color | White (`#FFFFFF`) |
| Outline | 1.5px solid black |
| Shadow | 1.5px semi-transparent black (alpha 80) |
| Position | Bottom-centered |
| Margin from bottom | 50px |
| Border style | 1 (outline + shadow, no box) |

In libass `force_style` syntax:

```
Fontname=Helvetica,Fontsize=24,Bold=1,
PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H80000000,
BorderStyle=1,Outline=1.5,Shadow=1.5,
Alignment=2,MarginV=50
```

This spec was iterated on with side-by-side comparisons of 19/22/24/26pt and
hard-outline vs soft-shadow variants. **Do not change without re-A/Bing on a
real clip.**

## Transcript cache (efficiency layer)

Whisper transcription is the slow step (~10-15s on a 60s clip, ~3-5min on a
full hour podcast). To avoid re-running whisper for every clip from the same
source, the pipeline caches a **full-podcast transcript keyed by YouTube
video ID**:

```
~/ytclipper-fast/transcripts/<VIDEO_ID>.srt        # sentence-level — caption display
~/ytclipper-fast/transcripts/<VIDEO_ID>.words.srt  # word-level — cue resolution & onset snap
~/ytclipper-fast/transcripts/<VIDEO_ID>.lock       # present while transcribing
```

The `.words.srt` is also consumed by `scripts/cue_to_timestamp.py` — when present,
it replaces YouTube auto-captions as the source of truth for resolving clip
start/end cues. This snaps the cut to actual word onsets (~50ms accuracy vs
~300ms for YouTube VTT) and eliminates the "trim 0.3s off the start" iteration.

### Pre-warming

`extract_clip.sh` triggers `transcribe_source.sh <VIDEO_ID>` in the background
the first time it downloads a source. By the time the user approves the post
and we caption the clip, the full-podcast SRT is usually ready.

### Caption-time behavior

`caption_clip.sh` looks for the cached SRT and picks the fastest path:

| Cache state | Behavior | Time |
|---|---|---|
| SRT present | Slice by `[clip_start, clip_start + clip_duration]`, offset to 0, burn | **~3-5s total** |
| SRT missing or `.lock` present | Run whisper.cpp on the clip directly, burn | ~15-20s total |

Either path produces an identical-quality result. The cache is purely a
speed optimization.

### Cache invalidation

Cached transcripts are immutable per video ID — YouTube videos don't change
content under a stable ID. To force a re-transcribe, delete:

```
rm ~/ytclipper-fast/transcripts/<VIDEO_ID>.srt
```

`transcribe_source.sh` is idempotent and the lock file is cleared on exit
(including crashes).

## Dependencies

The captioning scripts shell out to:

- **whisper.cpp** binary + `ggml-small.en.bin` model
  - default `$HOME/Desktop/AI Agents/remotion-captions/whisper.cpp/main`
  - override with env `WHISPER_BIN` and `WHISPER_MODEL`
- **ffmpeg with libass + libfreetype** (the stock Homebrew `ffmpeg` is built
  without these — every burn-in needs the static build)
  - default `$HOME/Desktop/AI Agents/remotion-captions/ffmpeg-full`
  - override with env `FFMPEG_FULL`

If either binary is missing, `caption_clip.sh` exits with a clear error
message. **Do not silently skip captioning** — surface the failure to the user.

## Why small.en instead of medium.en

We A/B'd on a 73s Musk clip:

- `medium.en` with `--max-len 42 --split-on-word`: ~6.5 min transcribe
- `small.en` with native segments: ~10-12s transcribe, no accuracy loss on
  clean podcast speech

`small.en` is the right size for clear-speech English podcast extraction. Bump
to `medium.en` only if you start seeing transcription errors on real clips
(unlikely with the speakers in our content rotation).

## Why sentence-level not word-by-word

Per `feedback`-level decisions, the @GeniusGTX feed reads more editorial than
TikTok-style. Word-by-word karaoke (Remotion + `createTikTokStyleCaptions`)
adds visual noise without measurable lift on the kind of dense, authority-led
posts we publish. Sentence-level captions, cinema-style, fit the brand.

The Remotion path stayed alive in `remotion-captions/` as a one-off tool for
hero clips that warrant per-clip styling. It is **not** the production
pipeline.
