# Install — one-time setup

## 1. System dependencies (macOS)

```bash
# yt-dlp for source video download
brew install yt-dlp

# ffmpeg for clip cutting and (optionally) caption burning
# Note: Homebrew's ffmpeg is fine for cutting (libx264 included).
# If you need burned-in captions, you also need libass + libfreetype.
# Easiest: copy the bundled ffmpeg-static from a YouTube Clipper FAST install,
# or `brew install ffmpeg` works for most cases.
brew install ffmpeg
```

## 2. Notion integration

1. Go to https://www.notion.so/my-integrations
2. Create a new internal integration. Name it whatever (e.g., "Goku Extraction").
3. Copy the secret token (`ntn_…`).
4. In Notion, open your **Evergreen Backlog** database.
5. Click `…` → `Connections` → add the integration.
6. Save the token to `.env` as `NOTION_TOKEN`.
7. Get the data source ID by opening the database in a browser:
   - URL pattern: `https://www.notion.so/<workspace>/<database_id>?v=<view_id>`
   - The data source ID is what `<database_id>` resolves to (32-char hex). Save as `NOTION_EVERGREEN_DS_ID`.

The database schema this expects (with property types):

| Property | Type |
|---|---|
| Video Title | title |
| Video URL | url |
| Source URL | url |
| Status | select (`Backlog` / `Adding Media` / `Ready to Post` / `Scheduled` / `Published` / `Killed`) |
| Topic Tags | multi_select |
| Parent item | relation (self-relation, limit 1) |
| Sub-item | relation (self, reverse) |
| Clip Start | text |
| Clip End | text |
| Key Quote | text |
| Typefully Shared URL | url |
| Typefully Draft ID | text |

See `config/notion-schema.json` for the full reference.

## 3. Typefully integration

1. Go to typefully.com → Settings → API.
2. Create or copy your API key.
3. Save to `.env` as `TYPEFULLY_API_KEY`.
4. Get your social set ID:
   - List social sets via the API: `GET /v1/social-sets`
   - Or in the Typefully URL when viewing a social set
   - Save as `TYPEFULLY_SOCIAL_SET_ID`

## 4. Clip storage

By default, the pipeline writes to:

```
~/ytclipper-fast/sources/    # cached full-length source videos (persistent, deep-nested — they're huge)
~/Desktop/AI Agents/clips/   # cut clips (user-facing — you drag-drop these into Typefully)
```

Why split? Source videos are 500–1500 MB and you don't interact with them directly. Cut clips are ~10–25 MB and you drag them into Typefully drafts. The clips folder lives on the Desktop in plain sight; the sources folder stays out of the way.

Override either via env vars: `SOURCES_DIR=...` and `CLIPS_DIR=...`.

**Don't put `SOURCES_DIR` in `/tmp` or any temp folder.** Those get cleaned across sessions and force a 3-min re-download each time.

## 5. Verify

```bash
set -a; source .env; set +a
bash scripts/extract_clip.sh https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:00:30 00:00:45
ls ~/ytclipper-fast/clips/
```

If you see a 15-second clip, the local pipeline works.

```bash
python3 scripts/notion_upload.py <test_page_id> ~/ytclipper-fast/clips/<file> test.mp4
```

If you see a video block on the test page, the Notion path works.
