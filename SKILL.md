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
4. **Draft the post** in strict Goku style. Read these in order:
   - `style/master-prompt.md` — the canonical Goku format
   - `style/closer-template.md` — the current 4-part closer
   - `style/clip-selection.md` — the clip start-cue rules
5. **Word-count the body** before delivering. ≤250 words, target 180–210.
6. **Pick a clip range + start/end cues.** Verbatim phrases, not just timestamps. Start cue must pass the standalone-hook test.
7. Show the draft to the user. **Wait for "Approved" before Phase 2.**

## Phase 2 — Operational Execution

When user approves, execute in parallel batches:

1. **Notion sub-item create** in Evergreen Backlog (status `Adding Media`, parent relation to source video).
2. **Typefully draft create** on the configured social set (X enabled, unscheduled, share=true).
3. **Clip extraction** in background via `scripts/extract_clip.sh URL START END` — uses fast keyframe seek (`-ss` BEFORE `-i`) and codec copy. Runs in ~1 second.
4. **When clip lands:**
   - `scripts/notion_upload.py PAGE_ID FILE NAME` — multi-part upload to Notion, attaches as native video block.
   - `scripts/typefully_upload.py SOCIAL_SET_ID DRAFT_ID FILE NAME` — presigned S3 PUT, polls media status, attaches to draft. Note: Typefully server-side video processing takes 5–15 min.
5. **Cross-link** Typefully URL/ID into Notion sub-item properties.
6. **Update parent backlog**: check the corresponding extractable-idea checkbox with link to the new sub-item.
7. **Advance Notion status** `Adding Media` → `Ready to Post` once both Notion and Typefully attaches succeed.

## Race condition warning (must surface to user)

Typefully UI edits can strip media attachments saved via API. After ANY API attach, tell the user: "Don't hand-edit the Typefully draft until you refresh first."

## Iteration

After Phase 2 confirms, ask the user: "Ship next idea?" and offer the next candidate from the original list. Default to ideas that connect with named figures the audience knows (the data shows Elon-connected posts perform best for @GeniusGTX).

## When the source is exhausted

After 5–10 posts, the same interview is mined out. Recommend pivoting to a new source video.
