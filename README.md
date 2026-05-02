# goku-extraction-pipeline

Turn one long-form video interview (Andreessen-style podcast, 1–2 hours) into 5–10 short-form X posts in the **@ProjectGokuu / @GeniusGTX style**, end-to-end automated.

## What this does

Given a YouTube URL + transcript, the pipeline:

1. **Extracts** 5–10 high-leverage Goku-style post angles from the source.
2. **Drafts** each post with the strict Goku format: credentialed-authority hook, named-character body, direct quotes, brand + product CTAs.
3. **Cuts** a 1–4 minute video clip per post using a fast keyframe-seek `ffmpeg` flow.
4. **Uploads** the clip natively to Notion (multi-part File Upload API) and to Typefully (presigned S3 + media attach).
5. **Cross-links** everything: Notion ↔ Typefully ↔ source video.
6. **Advances** Notion sub-item status to `Ready to Post` once media is attached.

## Why it exists

Built for [@GeniusGTX](https://x.com/GeniusGTX) — a content account on the greatest minds in economics, psychology, and history. The team was running this manually. This repo bundles it as a portable AI skill that any agent (Claude Code, Hermes, custom GPT) can invoke.

## Repo layout

```
goku-extraction-pipeline/
├── SKILL.md                    # entry point for AI agents
├── README.md                   # this file
├── INSTALL.md                  # one-time setup
│
├── style/                      # the "Goku" style system (markdown only)
│   ├── master-prompt.md        # the canonical Goku Analysis & Prompt
│   ├── closer-template.md      # current 4-part closer (engagement Q → brand → P.S. → attribution)
│   ├── clip-selection.md       # standalone-hook rule for clip openers
│   └── extraction-workflow.md  # Phase 1 (draft) → Phase 2 (operational) protocol
│
├── scripts/                    # helpers (bash + Python stdlib only)
│   ├── extract_clip.sh         # ffmpeg fast keyframe seek + codec copy
│   ├── notion_upload.py        # Notion multi-part File Upload + video block attach
│   └── typefully_upload.py     # Typefully presigned URL flow
│
├── config/
│   ├── .env.example            # NOTION_TOKEN, TYPEFULLY_KEY, social_set_id, paths
│   └── notion-schema.json      # Evergreen Backlog property names + IDs
│
└── examples/
    └── andreessen-interview/   # 8 posts extracted from one Andreessen interview
```

## Quickstart

1. `cp config/.env.example .env` and fill in your tokens.
2. Source: `set -a; source .env; set +a`
3. See `INSTALL.md` for prerequisites (`yt-dlp`, `ffmpeg`, Notion integration).
4. From an AI agent (Claude Code, Hermes, etc.): point it at `SKILL.md` and feed it a video URL + transcript.

## Status

v0.1 — works end-to-end on the GeniusGTX setup. Next: caption support (whisper auto-timing) and source-agnostic generalization.

## Credits

- [@ProjectGokuu](https://x.com/ProjectGokuu) — the style this is based on
- [@GeniusGTX](https://x.com/GeniusGTX) — the account this serves
