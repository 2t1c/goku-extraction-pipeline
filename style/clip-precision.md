# Clip Precision — cuts within 100ms of the verbatim cue

The problem: clips were landing 3–10 seconds off the verbatim start/end cues. Diagnosis below, plus the fixes that close the gap.

## Why clips drift

Two compounding sources of error:

**(1) Transcript timestamps are chunk-level, not word-level.** The transcript surfaced in source material (e.g. Merlin AI exports for the Dwarkesh podcast) groups 2–7 seconds of audio under a single timestamp. Reading `33:50` off the transcript and passing it to `extract_clip.sh` is already a guess — the actual moment the cue is spoken sits *somewhere inside* that 2–7 second window, biased toward the end if the line is long.

**(2) ffmpeg fast-seek snaps to keyframes.** `extract_clip.sh` uses `-ss` BEFORE `-i` with `-c copy` for ~600× realtime speed. That snaps the cut to the nearest preceding keyframe, which on YouTube source material can be another 1–5 seconds early. Net drift: requested `33:50`, audio actually at `33:53.8`, ffmpeg cuts at `33:48` (keyframe).

By the time both errors stack, the clip can start mid-sentence on a transitional filler instead of on the arresting hook the cue was chosen for.

## Solutions, ranked by impact

### (T1) Cue-lookup via cached YouTube captions — **landed**

`scripts/cue_to_timestamp.py` parses cached `.en.vtt` auto-captions and fuzzy-matches the cue's first 3–10 words against the caption stream (lowercased alphanumerics). Returns `START_TS=HH:MM:SS.mmm` with 0.3s head padding and 0.5s tail padding. Caches the .vtt in `~/ytclipper-fast/sources/<video_id>.en.vtt` on first call via `yt-dlp`.

The bug was that `extract_clip.sh` doesn't call it. Drivers (humans or agents) were passing timestamps directly, often eyeballed off the chunked transcript.

### (T2) Frame-accurate two-pass ffmpeg cut — **landed**

`scripts/extract_clip_tight.sh` is the new default extraction entry point. Combines T1 + T2:

1. Calls `cue_to_timestamp.py` to resolve cues → ms-accurate timestamps
2. Pass 1: fast `-ss BEFORE -i` keyframe seek + `-c copy` for a coarse 10-second-buffer slice (~5MB)
3. Pass 2: accurate `-ss AFTER -i` seek inside the small coarse file with re-encode (`libx264 preset fast crf 22`)

Total cut time: ~5–10 seconds on cached source. Worth the ~5× slowdown vs the legacy keyframe-aligned cut for the precision gain.

```bash
extract_clip_tight.sh \
  "https://www.youtube.com/watch?v=BYXbuik3dgA" \
  "Can you imagine some mass driver" \
  "create the solar cells and the radiators on the moon" \
  musk-mass-driver-moon
```

`extract_clip.sh` stays around for legacy callers and for cuts that don't correspond to a single spoken phrase (B-roll, music). All new pipeline calls should use `extract_clip_tight.sh`.

### (T3) Boundary validation with whisper-tiny — proposed

After the cut, run whisper-tiny on the first and last 3 seconds. Verify:

- First 3s contains ≥4 of the start cue's first 6 words
- Last 3s contains ≥3 of the end cue's last 5 words

If either fails, log the drift and either retry with a 1-second-earlier start (auto-heal) or surface the warning to the operator. Catches caption-vs-audio mismatches automatically.

Implementation cost: ~50 lines of Python, ~200ms per validation on M-series Mac with whisper.cpp. Defer until we see a T1+T2 failure that this would have caught.

### (T4) VAD-based silence snapping — proposed

Use Silero VAD or webrtcvad to find the silence gap nearest the requested cut point. Snap to silence so cuts always land between sentences instead of mid-syllable. Eliminates the "starts on a stray consonant" failure mode.

Roughly 100ms refinement on top of T1+T2+T3. Diminishing returns; defer.

### (T5) Cue normalization edge cases

`cue_to_timestamp.py` already lowercases and strips punctuation. Known gaps:

- **Contractions:** auto-captions use "don't" while a hand-written cue might say "do not". The fuzzy matcher won't bridge that.
- **Numerics:** "1.5 GB" in the cue vs "one point five gigabytes" in the captions. Different lexemes entirely.
- **Filler words:** "I, uh, just want to" in audio vs "I just want to" in the cue.

When cues fail to resolve, the operator should re-write the cue as the captions actually transcribe the line, not as the line "should" read.

## Pipeline rule

The default extraction call is now:

```bash
extract_clip_tight.sh <url> "<start_cue>" "<end_cue>" <slug>
```

Operators should only fall back to `extract_clip.sh <url> <HH:MM:SS> <HH:MM:SS> <slug>` for:

- Videos without auto-captions (live streams, very recent uploads, age-restricted)
- Cuts that don't correspond to a single spoken phrase (B-roll segments, music)

## Audit checklist additions

When `extract_clip_tight.sh` lands as the default, update `post-quality-checklist.md` clip section:

- [ ] Clip extracted via `extract_clip_tight.sh` (cue-driven), not raw timestamps
- [ ] First 3 seconds of clip contain start cue verbatim (manual or whisper-validated)
- [ ] Last 3 seconds of clip contain end cue verbatim
