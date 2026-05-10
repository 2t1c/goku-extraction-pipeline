# Clip Precision — cuts within 100ms of the verbatim cue

The problem: clips were drifting 3–10 seconds off the verbatim start/end cues. Diagnosis below, plus the fixes that close the gap.

## Why clips drift

Two compounding sources of error in the legacy pipeline:

**(1) Transcript timestamps are chunk-level, not word-level.** The transcript surfaced in source material (e.g. Merlin AI exports for the Dwarkesh podcast) groups 2–7 seconds of audio under a single timestamp. Reading `33:50` off the transcript and passing it to `extract_clip.sh` is already a guess — the actual moment the cue is spoken sits *somewhere inside* that 2–7 second window.

**(2) ffmpeg fast-seek snaps to keyframes.** `extract_clip.sh` uses `-ss` BEFORE `-i` with `-c copy` for ~600× realtime speed. That snaps the cut to the nearest preceding keyframe, which on YouTube source material can be another 1–5 seconds early. Net drift: requested `33:50`, audio actually at `33:53.8`, ffmpeg cuts at `33:48` (keyframe).

By the time both errors stack, the clip can start mid-sentence on a transitional filler instead of on the arresting hook the cue was chosen for.

## What's landed

### (T1) Word-stream cue lookup — `cue_to_timestamp.py`

Parses the cached YouTube `.en.vtt` into a flat `[(timestamp, word), ...]` stream using the inline word-level timestamps (`<HH:MM:SS.sss><c> word</c>`). Drops static caption blocks (≈10 ms duration) and de-duplicates leading-text repeats from rolling caption windows. Result: ~25k unique words for a 3-hour podcast, each with millisecond accuracy.

**Filler stripping** in `norm()` handles `uh`/`um`/`er`/`ah`/`hm`/`you know`/`i mean`/`sort of`/`kind of`/`like`. Both cue text and stream go through the same filter.

**Punctuation stripped in-place** so `40,000` matches `40000`, `I'm` matches `im`. Matches how YouTube's ASR typically emits numbers and contractions.

**Skip tolerance in the matcher** — when matching the cue's first 8 tokens against the stream, allow up to 2 missed tokens. Catches `one` vs `1`, `gigabytes` vs `gb`, mistranscribed proper nouns. Threshold for accepting a candidate: `j ≥ n_target - 2`.

**Bidirectional disambiguation** — resolve the END cue first (usually more distinctive), then use its timestamp as an auto-near-hint when searching for the START cue. Cuts the ambiguity rate without operator intervention.

**Loud failure on ambiguity** — when multiple candidate matches survive de-duplication and no `near_sec` hint is provided, the resolver exits with code 4 and prints all candidate timestamps. The wrapper script surfaces this and demands a hint.

Validation pass on 10 real cues from the shipped Musk pipeline: **8/10 resolve cleanly**, 2/10 produce candidate-list errors that resolve with a `near` hint.

### (T2) Frame-accurate two-pass cut — `extract_clip_tight.sh`

The new pipeline default. Combines T1 with a frame-accurate cut:

1. Calls `cue_to_timestamp.py` to resolve cues → ms-accurate timestamps
2. Pass 1: fast `-ss BEFORE -i` keyframe seek + `-c copy` for a coarse 5–15 MB slice with 10s tail buffer
3. Pass 2: accurate `-ss AFTER -i` seek inside the small coarse file with re-encode (`libx264 preset fast crf 22`)

Total cut time: ~30–90 seconds per clip on cached source (mostly Pass 2 re-encoding). Worth the trade vs ~1s for keyframe-aligned cuts in `extract_clip.sh`.

```bash
extract_clip_tight.sh \
  "https://www.youtube.com/watch?v=BYXbuik3dgA" \
  "It's having the heat shield be reusable" \
  "laborious inspection of 40,000 tiles" \
  musk-heat-shield-kills-starship
```

Optional 5th argument is `near_seconds` — pass when the cue could match in multiple places.

### (T3) Whisper boundary validation — `validate_boundaries.py`

Optional post-cut step. Transcribes the first 4 seconds and last 4 seconds of the cut clip with `mlx-whisper` (Apple Silicon), `faster-whisper` (cross-platform), or `whisper-cpp` (binary), and fuzzy-matches the transcription against the expected start/end cues.

If no whisper is installed, the script no-ops with a one-line note. Wired into `extract_clip_tight.sh` as a final step.

To enable:
```
pip install mlx-whisper        # macOS Apple Silicon (recommended)
pip install faster-whisper     # cross-platform
brew install whisper-cpp       # macOS Homebrew binary
```

`extract_clip.sh` stays around for cuts that don't correspond to a single spoken phrase (B-roll, music) and for legacy callers.

## Remaining gotchas

### (G1) Cues must match what captions actually transcribe

Auto-captions reflect ASR errors and stylistic choices: `1` not `one`, `gb` not `gigabytes`, mistranscribed proper nouns (`Dwarkesh` → `dwar cash`, `Heinlein` → `heinline`). The skip-tolerant matcher absorbs ~2 such mismatches per 8-token target window, but a cue with 4+ words wrong won't resolve.

When a cue fails to resolve, fix it by checking the actual `.en.vtt` near the expected timestamp. Operator-readable command:

```bash
grep -A1 "02:09:3" ~/ytclipper-fast/sources/<video_id>.en.vtt
```

### (G2) Ambiguous cues need a near_seconds hint

When the cue's prefix matches multiple distinct locations (e.g. "It's the vanes and blades in the turbines" — Musk repeats this 5 times), the resolver exits with code 4 and lists all candidates. The operator picks the right one and re-runs with the approximate timestamp:

```bash
extract_clip_tight.sh URL "start cue" "end cue" slug 350
#                                                     ^^^ ~5:50
```

### (G3) Ambiguity heuristic is end-cue-first

The resolver picks the END cue first and uses its timestamp as a hint for the START cue. This works when the end cue is unique and the clip is short (≤4 minutes between them). For longer clips or when the start cue is the unique one, use a `near_seconds` hint that's closer to the start.

## Audit checklist

`post-quality-checklist.md` should add to the clip section:

- [ ] Clip extracted via `extract_clip_tight.sh` (cue-driven), not raw timestamps
- [ ] First 3 seconds of clip contain start cue verbatim (manual check or whisper validation)
- [ ] Last 3 seconds of clip contain end cue verbatim
- [ ] If `extract_clip_tight.sh` exited with `AMBIGUOUS=...`, the chosen `near_seconds` hint corresponds to the intended occurrence
