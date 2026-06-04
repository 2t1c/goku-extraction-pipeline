# Install — one-time setup

## 1. System dependencies (macOS)

```bash
# yt-dlp for source video download
brew install yt-dlp

# ffmpeg for clip cutting (Homebrew's build is fine — it includes libx264).
brew install ffmpeg
```

> **Captions are optional.** The default student path ships clips **without** burned-in
> captions — you cut the clip and drag it into Typefully. You can add captions on X/Typefully,
> or set up local caption burning later (see §6, advanced). Don't let captions block your first post.

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
~/Desktop/goku-clips/   # cut clips (user-facing — you drag-drop these into Typefully)
```

Why split? Source videos are 500–1500 MB and you don't interact with them directly. Cut clips are ~10–25 MB and you drag them into Typefully drafts. The clips folder lives on the Desktop in plain sight; the sources folder stays out of the way.

Override either via env vars: `SOURCES_DIR=...` and `CLIPS_DIR=...`.

**Don't put `SOURCES_DIR` in `/tmp` or any temp folder.** Those get cleaned across sessions and force a 3-min re-download each time.

## 5. Verify

```bash
set -a; source .env; set +a
bash scripts/extract_clip.sh "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 00:00:30 00:00:45
ls ~/Desktop/goku-clips/
```

> **Quote the URL.** macOS's default shell (zsh) treats `?` in the URL as a wildcard — an
> unquoted URL fails with `zsh: no matches found`. Always wrap YouTube URLs in `"…"`.

If you see a 15-second clip in `~/Desktop/goku-clips/`, the local pipeline works.

```bash
python3 scripts/notion_upload.py <test_page_id> ~/Desktop/goku-clips/<file> test.mp4
```

If you see a video block on the test page, the Notion path works.

## 6. Captions (optional, advanced)

The default path ships clips without burned-in captions. To burn them locally you need three
things, then run `scripts/caption_clip.sh <clip-path> <video-id> <clip-start-HH:MM:SS>`:

1. **whisper.cpp** — `brew install whisper-cpp` (installs `whisper-cli`).
2. **A model** — download once:
   ```bash
   mkdir -p ~/ytclipper-fast/models
   curl -L -o ~/ytclipper-fast/models/ggml-base.en.bin \
     https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
   ```
3. **An ffmpeg with libass** (the `subtitles` filter). Homebrew's ffmpeg may not include it —
   verify with `ffmpeg -hide_banner -filters | grep subtitles`. If it's missing, point
   `FFMPEG_FULL` at an ffmpeg build that has it.
