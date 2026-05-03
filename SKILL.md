---
name: goku-extraction-pipeline
description: Extract short-form X posts in the @ProjectGokuu / @GeniusGTX style from long-form video interviews. Drafts posts, cuts video clips, uploads to Notion (Evergreen Backlog) and Typefully drafts, cross-links everything.
trigger_phrases:
  - "extract Goku post"
  - "extract from this podcast"
  - "/goku-extract"
  - "run extraction pipeline"
inputs_required:
  - YouTube URL or video file
  - Full transcript with inline timestamps (MM:SS or HH:MM:SS)
  - Notion integration token (env: NOTION_TOKEN)
  - Typefully social set ID (env: TYPEFULLY_SOCIAL_SET_ID)
  - Notion Evergreen Backlog parent data source ID (env: NOTION_EVERGREEN_DS_ID)
---

# Goku Extraction Pipeline — Skill

When the user invokes this skill (via trigger phrase, slash command, or `/goku-extract`), execute the following workflow.

## Phase 1 — Ideation & Drafting

For each candidate post idea from the source:

1. **Read** the full transcript. Don't skim — find Tier 1 angles that hit the Goku virality stack (authority + shocking specific claim + named characters + suppression layer).
2. **Surface 5–10 candidate ideas** ranked by tier (1 = potential 500K+, 2 = 100K–500K, 3 = 50K–150K). Show them to the user with one-line rationales.
3. **User picks one.** Don't draft until they confirm.
4. **Draft the post** in strict Goku style. Read these IN ORDER, every time:
   - `style/master-prompt.md` — the canonical Goku format (current rules, supersedes any older Goku doc)
   - `style/hook-recipe.md` — the violent-verb hook formula. **Read this before writing any hook.**
   - `style/body-techniques.md` — number cascades, dialogue exchanges, closing paradoxes, speaker stake in prose
   - `style/word-count.md` — target 240–250 words, not 180–210
   - `style/no-recency-words.md` — no `just`, `now`, `today`, `recently`, `this week`
   - `style/closer-template.md` — engagement Q + brand + P.S. + attribution
   - `style/clip-selection.md` — standalone-hook rule for the clip start cue
   - `style/notion-card-rendering.md` — Notion cover image + quote rendering rules
   - `examples/andreessen-interview/extracted-posts/` — what good looks like (H, A, I are the gold standards)
5. **Word-count the body before delivering.** Target 240–250 words. Don't estimate — count. If short, pull more substance from the transcript per `word-count.md` (secondary characters, parallels, backstory) — never pad with filler.
6. **Run the post quality checklist** at `style/post-quality-checklist.md`. Every box must check before showing the user. The most-violated rules in practice: (a) bland verb in hook (`built`, `created`, `revealed` instead of `killed`, `crushed`, `lit on fire`), (b) recency words sneaking in, (c) credential paragraph at body open instead of speaker-stake-in-prose.
7. **Pick a clip range + start/end cues.** Verbatim phrases. Start cue passes the standalone-hook test.
8. Show the draft to the user. **In the same turn, kick off `bash scripts/extract_clip.sh URL START END <slug> &` in background** — the user nearly always approves with minimal edits, and parallel pre-cutting eliminates the ffmpeg wait from Phase 2. Use a descriptive slug (e.g. `andreessen-ovitz-7am-meeting`) per `feedback_clip_naming_convention`.
9. **Wait for "Approved" before creating Notion / Typefully artifacts.** Local clip files are safe to pre-create; workspace objects are not.

## Phase 2 — Operational Execution

When user approves, execute in parallel batches:

1. **Notion sub-item create** in Evergreen Backlog (status `Adding Media`, parent relation to source video).
2. **Typefully draft create** on the configured social set (X enabled, unscheduled, share=true).
3. **Clip extraction** in background via `scripts/extract_clip.sh URL START END` — uses fast keyframe seek (`-ss` BEFORE `-i`) and codec copy. Runs in ~1 second.
4. **When clip lands:**
   - `scripts/notion_upload.py PAGE_ID FILE NAME` — multi-part upload to Notion, attaches as native video block. **Fully automated.**
   - **Typefully parallel API (default):** `POST /v1/media-uploads` then `curl -T FILE PRESIGNED_URL`. Fire and move on. Don't block on encoding. At batch checkpoints, poll pending media_ids and PATCH drafts when each is `ready`. Manual drag-drop only if user explicitly asks or API fails.
5. **Cross-link** Typefully URL/ID into Notion sub-item properties (text-only — the URL is known the moment the draft is created).
6. **Update parent backlog**: check the corresponding extractable-idea checkbox with link to the new sub-item.
7. **Advance Notion status** `Adding Media` → `Ready to Post` once the Notion video block is attached and Typefully PUT is fired.

## Final user-facing message

When you finish Phase 2, surface to the user:
- Notion sub-item URL (Status `Ready to Post`)
- Typefully draft URLs (text already attached, media PUT fired and processing)
- Local clip path (manual drag-drop escape hatch): `~/Desktop/AI Agents/clips/<filename>.mp4`
- **Lockout warning**: "Don't hand-edit any pending Typefully drafts until I confirm all media attaches landed."

## Manual drag-drop fallback

If user explicitly asks for manual or API fails: surface the local clip path. They drag the .mp4 onto the draft in browser (~10 sec). `scripts/typefully_upload.py` is also available for headless full-automation runs.

## Race condition warning (load-bearing)

Typefully UI edits between the PUT and the final PATCH attach can strip media_ids. Tell the user explicitly: "Don't touch the pending Typefully drafts until I confirm attaches landed." Lockout window is the slowest single clip's encoding time (5–15 min).

## Iteration

After Phase 2 confirms, ask the user: "Ship next idea?" and offer the next candidate from the original list. Default to ideas that connect with named figures the audience knows (the data shows Elon-connected posts perform best for @GeniusGTX).

## When the source is exhausted

After 5–10 posts, the same interview is mined out. Recommend pivoting to a new source video.
