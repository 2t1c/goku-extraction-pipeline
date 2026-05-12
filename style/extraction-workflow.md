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

### 1.4 Show draft + wait + pre-cut clip in background

Deliver post + clip spec to the user. **In the same turn, kick off the clip extraction in background:**

```bash
bash scripts/extract_clip.sh URL START END &
```

The user almost always approves with zero or minimal edits. By the time they say "Approved," the clip file should already exist on disk — so Phase 2 skips straight to upload without an ffmpeg wait. With cached source video the cut is ~1 second, but on the first clip of a session it's 2–4 min, and that's exactly the wait worth eliminating from the user's path.

**Don't pre-cut on the ideation menu** (Phase 1 step 1.2). Multiple candidates are surfaced; only one gets drafted; cutting all wastes work.

**Don't pre-create Notion sub-items or Typefully drafts.** Those are real workspace artifacts. Pre-cutting only the local clip file is safe — it can be deleted if the post is killed.

If the user revises the clip range during review, re-cut. It's cheap.

**Wait for "Approved" or equivalent before Phase 2 of the workspace artifacts.**

## Phase 2 — Operational Execution (mostly parallel)

When approved, execute in this order. Steps in `()` parens are parallel-safe.

### 2.1 Setup (parallel — fire all 3 at once)

1. **Create Notion sub-item** in Evergreen Backlog. Status = `Adding Media`. Set: Video Title, Video URL, Source URL, Topic Tags, Clip Start, Clip End, Key Quote, Parent item relation. Body content = full post draft + clip spec. **The Clip Spec section's `Local clip path:` line must be rendered as a `file://` hyperlink so it opens in Finder on click** — format: `[~/Desktop/AI Agents/clips/<slug>.mp4](file:///Users/toantruong/Desktop/AI%20Agents/clips/<slug>.mp4)` (URL-encode every space as `%20`). See `style/notion-card-rendering.md` §3.
2. **Create Typefully draft** on the configured social set. X platform enabled, unscheduled, share=true. Scratchpad = source URL + clip cues + parent video URL + (sub-item URL once known).
3. **Cut the clip** via `scripts/extract_clip.sh URL START END` — fast keyframe seek + codec copy. Background process. Outputs to `~/ytclipper-fast/clips/`.

### 2.2 Cross-link (after 2.1 returns)

1. Patch the Notion sub-item with `Typefully Shared URL` + `Typefully Draft ID`.
2. Patch the Typefully scratchpad with the Notion sub-item URL.
3. Update the parent video page's "extractable ideas" checklist — check the corresponding box and add a link to the new sub-item.

### 2.3 Upload media — Notion API + Typefully parallel API (default)

When the clip file exists:

1. **Notion (automated):** `python3 scripts/notion_upload.py PAGE_ID FILE NAME` — multi-part File Upload API + attach as native video block. ~10–20 sec per file.
2. **Typefully (parallel API, automated):** Fire the PUT immediately. Don't block on the encoding queue.
   - `POST /v1/media-uploads` → presigned S3 URL + media_id (instant)
   - `curl -T FILE PRESIGNED_URL` (PUT, raw bytes, no headers — instant for 10–25 MB clips)
   - **Move on to next post immediately.** Don't poll.
3. **At batch checkpoints** (every 2–3 posts, or at end of session):
   - Poll all pending `media_id`s.
   - When each flips from `processing` to `ready`, `PATCH /v1/drafts/<draft_id>` with `media_ids: [<media_id>]` and the unchanged post text.

**Why parallel API:** Typefully encodes clips concurrently on their backend, so total wall-clock for N clips is the slowest single clip's processing time (5–15 min), not N × 5–15 min. That's hands-free *and* faster than manual drag-drop, which is unreliable and still costs user time per post.

**Race condition warning (load-bearing):** the user MUST NOT hand-edit Typefully drafts between the PUT and the final PATCH. UI saves can strip media_ids. Tell them explicitly: "Don't touch these drafts until I confirm attaches landed." Lockout window is the slowest clip's encoding time.

**Manual drag-drop fallback:** if user explicitly asks for manual, or if the API path fails, surface the local clip path as a `file://` hyperlink (`[~/Desktop/AI Agents/clips/<filename>.mp4](file:///Users/toantruong/Desktop/AI%20Agents/clips/<filename>.mp4)`) and the draft edit URL. They click the hyperlink to reveal the clip in Finder, then drag it in. `scripts/typefully_upload.py` still works for headless runs.

### 2.4 Finalize

When the Notion video block is attached AND the Typefully PUT has been fired:

1. Patch Notion sub-item Status: `Adding Media` → `Ready to Post`.
2. Tell the user the Notion + Typefully URLs and the local clip path (in case they want manual escape).
3. **Warn**: "Don't hand-edit any of the pending drafts in Typefully until I confirm all attaches finished."
4. Ask: "Next idea?" or continue if user pre-approved a batch.

### 2.5 Append to Master Index (mandatory)

The [📚 Master Index — Evergreen Backlog](https://www.notion.so/35d04fca179481bd9c79d53bbd42838b) is the human discovery layer that bypasses Notion's weak database search. **Every Ready-to-Post draft must appear here.**

After the sub-item flips to `Ready to Post`:

1. Open the Master Index page (ID `35d04fca-1794-81bd-9c79-d53bbd42838b`).
2. Find the parent video's H2 section (e.g. `## 🎥 [Michael Dell on Founders Podcast — ...](...)`).
3. Append a new bullet at the bottom of that section: `- [<post-title>](<notion-sub-item-url>)`.
4. If the parent video section does not exist yet, create it as a new `## 🎥 [<video-title>](<parent-page-url>) · 1 draft` block, then add the bullet under it.
5. Bump the draft count in the section header (e.g. `· 8 drafts` → `· 9 drafts`).

**Refresh-from-scratch is also valid** when you want a clean rebuild: query the Evergreen Backlog data source via `notion-fetch` on `collection://316f17ad-ba4f-4719-b239-67a38141b0c9`, group by parent video, rebuild the entire page via `notion-update-page` with `replace_content`.

The user can also trigger a full refresh anytime by saying "refresh the master index" in any Claude chat.

### Workflow expectation

The user finds drafts in the Master Index (Ctrl-F on the page) → clicks the @mention → lands on the Notion card → copies the post body (in code block, one-click copy) and the attached clip → pastes into Typefully manually → schedules. The Master Index is the search-layer fix for Notion's database search being unreliable.

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
