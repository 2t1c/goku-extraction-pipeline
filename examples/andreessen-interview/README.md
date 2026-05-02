# Example — Marc Andreessen × David Senra interview

Source: [Marc Andreessen: The World Is More Malleable Than You Think](https://www.youtube.com/watch?v=qBVe3M2g_SA) (~109 min)

This example shows the pipeline running end-to-end on a single 109-minute Andreessen interview, producing **8 distinct Goku-style posts** for @GeniusGTX.

## The 8 posts extracted

| # | Hook | Tier | Clip range | Result |
|---|---|---|---|---|
| 1 | "Netscape founder Marc Andreessen says the greatest founders in history had zero introspection." | 1 | 1:03 – 4:45 | shipped |
| 2 | "Marc Andreessen just revealed how Harvard Business School was built on a broken 1941 theory, and how it's now collapsing..." | 1 | 12:39 – 16:30 | shipped |
| 3 | "Marc Andreessen says Elon Musk runs 120 design reviews a day in 5-minute slots." | 2 | 1:40:23 – 1:43:16 | shipped — **strong engagement** |
| 4 | "Marc Andreessen says Starlink was Elon's side project at the rocket company." | 1–2 | 1:47:31 – 1:49:08 | shipped |
| 5 | "Marc Andreessen says Elon almost lit his entire $180 million fortune on fire making rockets." | 1 | 1:45:01 – 1:46:50 | shipped |
| 6 | "Marc Andreessen says Sequoia's Mike Moritz passed on Tesla in 2008." | 2 | 1:42:55 – 1:44:00 | shipped |
| 7 | "Marc Andreessen says 2,000 American car companies launched in 10 years — only 3 survived." | 2 | 1:44:03 – 1:45:11 | shipped |
| 8 | "Marc Andreessen says he was personally tech support for the entire internet for three years." | 2 | 1:04:18 – 1:06:07 | shipped |
| 9 | "Marc Andreessen says the 1880 press warned women the bicycle would permanently freeze their faces." | 3 | 1:11:15 – 1:14:35 | shipped |

(See `extracted-posts/` for the full body text of each.)

## What we learned (lessons paid for in the field)

### Engagement signal
**Posts that name Elon outperform.** #3 (Elon 120 reviews) drove the strongest engagement, which validated the strategy of stacking 4 more Elon-connected posts (#4–#7). For @GeniusGTX, named-Elon hooks are a Tier 1 multiplier on top of whatever Goku tier the underlying claim sits at.

### Pipeline performance
1. **`ffmpeg -ss BEFORE -i + -c copy`** is 100–600× faster than the naive ordering. A 1:45 clip from a 109-min source: ~1 second instead of ~10 minutes.
2. **Persist source video** at `~/ytclipper-fast/sources/`. The `temp/` folder we used initially got cleaned across sessions, forcing a 3-min re-download.
3. **Fire all Typefully PUTs in parallel** as soon as clips exist. Server-side video processing is 5–15 min per file; parallel queueing saves wall-clock time.
4. **Notion file uploads >20 MB require multi-part.** Single-part caps at 20 MB. We use 10 MB chunks (over 5 MB min, under 20 MB max).

### Style refinements that improved the posts
1. **Dropped the bridge / reciprocity-lens section** from the closer. Old structure was 5 parts (engagement Q → bridge → product → brand → attribution). New is 4 parts (engagement Q → brand → P.S. product → attribution). Tighter.
2. **Spaced @handles in attribution** ( `@pmarca` instead of `@pmarca`). X's auto-mention engine needs the spaces to render mentions as clickable.
3. **Standalone hook rule for clip start cues.** A clip's first sentence must grab a cold scroller in 2–3 seconds. We learned this by shipping post #2's clip starting with *"The book that I always recommend..."* — a transitional setup that didn't hook. Banned that pattern thereafter.
4. **Don't hand-time captions.** First captioning attempt used hand-estimated SRT timings — drifted noticeably. Captions need real audio transcription (`mlx-whisper` recommended for Apple Silicon). Decided burned-in captions are optional, not default.

### MCP / API gotchas
- **Typefully UI race:** any UI edit after an API attach can strip the media_ids. Pattern is: API attach → user edits in browser without refreshing → user saves → media gone. Always tell the user to refresh first.
- **Two Typefully MCP namespaces** (`mcp__typefully__*` and `mcp__b641a33a-…__typefully_*`) flicker availability. Both work the same way — just hit whichever is connected.
- **macOS TCC blocks exec from `~/Downloads/`.** The original `clip.sh` lives there; we worked around by inlining its logic with system-installed `yt-dlp` + `ffmpeg`.

## Replicating

```bash
# From repo root
set -a; source .env; set +a

# Cut all 8 clips (assumes source already downloaded)
for spec in \
  "00:01:03 00:04:45" \
  "00:12:39 00:16:30" \
  "01:40:23 01:43:16" \
  "01:47:31 01:49:08" \
  "01:45:01 01:46:50" \
  "01:42:55 01:44:00" \
  "01:44:03 01:45:11" \
  "01:04:18 01:06:07" \
  "01:11:15 01:14:35"
do
  read START END <<< "$spec"
  bash scripts/extract_clip.sh "https://www.youtube.com/watch?v=qBVe3M2g_SA" "$START" "$END"
done
```

(The full automation — Notion sub-items, Typefully drafts, attaches, cross-links — is what `SKILL.md` invokes. See that file for the agent-driven flow.)
