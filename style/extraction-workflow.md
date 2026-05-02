# Extraction Workflow — Phase 1 → Phase 2

## Phase 1 — Ideation & Drafting (interactive)

### 1.1 Source intake

User provides:
- Video URL (YouTube)
- Full transcript with inline timestamps (MM:SS or HH:MM:SS)
- Optional: which Tier they're targeting (1, 2, 3) or which themes (e.g., Elon-connected)

### 1.2 Surface candidate ideas

Read the entire transcript. List 5–10 high-leverage angles. For each:
- One-line hook attempt in Goku format: `[Credentialed Name] says [shocking specific claim].`
- Tier estimate (1 = potential 500K+, 2 = 100K–500K, 3 = 50K–150K)
- Transcript range
- Why it works (one line)

Surface to user. Wait for them to pick.

### 1.3 Draft the chosen post

1. Read `style/master-prompt.md` — the full Goku format.
2. Read `style/closer-template.md` — the current 4-part closer.
3. Draft the post.
4. Word-count the body BEFORE delivering. ≤250 words, target 180–210. Don't estimate.
5. Run the virality stress test — see master-prompt.md, Part 11.
6. Pick a clip range + verbatim start/end cues per `style/clip-selection.md`.

### 1.4 Show draft + wait

Deliver post + clip spec. **Do not proceed to Phase 2 until user says "Approved" or equivalent.**

## Phase 2 — Operational Execution (mostly parallel)

When approved, execute in this order. Steps in `()` parens are parallel-safe.

### 2.1 Setup (parallel — fire all 3 at once)

1. **Create Notion sub-item** in Evergreen Backlog. Status = `Adding Media`. Set: Video Title, Video URL, Source URL, Topic Tags, Clip Start, Clip End, Key Quote, Parent item relation. Body content = full post draft + clip spec.
2. **Create Typefully draft** on the configured social set. X platform enabled, unscheduled, share=true. Scratchpad = source URL + clip cues + parent video URL + (sub-item URL once known).
3. **Cut the clip** via `scripts/extract_clip.sh URL START END` — fast keyframe seek + codec copy. Background process. Outputs to `~/ytclipper-fast/clips/`.

### 2.2 Cross-link (after 2.1 returns)

1. Patch the Notion sub-item with `Typefully Shared URL` + `Typefully Draft ID`.
2. Patch the Typefully scratchpad with the Notion sub-item URL.
3. Update the parent video page's "extractable ideas" checklist — check the corresponding box and add a link to the new sub-item.

### 2.3 Upload media — Notion API, Typefully manual (default)

When the clip file exists:

1. **Notion (automated):** `python3 scripts/notion_upload.py PAGE_ID FILE NAME` — multi-part File Upload API + attach as native video block. ~10–20 sec per file.
2. **Typefully (manual drag-drop, user does this):** Print the local clip path and the Typefully draft edit URL. The user drags the file onto the draft in their browser (~10 sec). Skip the API attach.

**Why manual for Typefully:** the API path forces a 5–15 min server-side video processing wait (sometimes 30+). Manual drag-drop bypasses the polling loop, avoids the UI race condition, and lets the user upload + edit in one session. Saves ~35 min per 5-post session.

**Optional fallback (fully automated):** `scripts/typefully_upload.py` still works — `python3 scripts/typefully_upload.py SOCIAL_SET_ID DRAFT_ID FILE NAME`. Use only when running headless or when the user explicitly asks for full automation.

### 2.4 Finalize

When the Notion video block is attached:

1. Patch Notion sub-item Status: `Adding Media` → `Ready to Post`. Don't wait on Typefully — that's the user's last touch.
2. Tell the user:
   - The local clip path: `~/ytclipper-fast/clips/<filename>.mp4`
   - The Typefully draft edit URL: `https://typefully.com/?d=<draft_id>&a=<social_set_id>`
   - The instruction: "Drag the file onto the draft when you're ready to ship."
3. Ask: "Ship next idea?"

## Phase 3 — Iteration

Default to ideas that connect with named figures the audience knows. For @GeniusGTX, Elon-connected posts have demonstrated highest engagement.

After 5–10 extractions from one source, the source is mined out. Recommend pivoting to a new video.

## Performance notes

These are the lessons paid for in the field:

1. **`-ss` BEFORE `-i`** in ffmpeg. Decode-and-discard seek is 100–600× slower than keyframe seek.
2. **Codec copy with `-c copy`** — source is already H.264/AAC. No re-encode. Cuts go from 30s → 1s.
3. **Persist source video** at `~/ytclipper-fast/sources/`. `temp/` and `/tmp/` get cleaned across sessions.
4. **Fire all Typefully PUTs in parallel** as soon as clips exist. Their server-side processing is 5–15 min per video — overlapping the queue saves wall-clock time.
5. **Notion multi-part upload required for files >20 MB**. Single-part caps at 20 MB; use 10 MB chunks for safety (over the 5 MB minimum, under the 20 MB max). See `scripts/notion_upload.py`.
6. **The Typefully UI race**: any UI edit after an API attach will strip the media. Always tell the user to refresh before editing.
