# Notion Card Rendering

Two rules govern the visual layer of every card the pipeline creates in Notion (parent video pages AND sub-item post pages). Both protect downstream copy-paste fidelity to X / Typefully and make the Evergreen Backlog gallery scannable at a glance.

## 1. Cover image — random pick from Notion's built-in gallery

Every page gets a `cover.external.url` set to one of Notion's stock cover-gallery URLs (the same images that appear in Notion's "Add cover" → "Gallery" picker).

**Do not** use YouTube thumbnails for covers. They make the gallery view visually noisy, the aspect ratio is wrong (16:9 thumbnails crop awkwardly into Notion's wide cover band), and a 30-card database where every card is a different YouTube screenshot is harder to scan than one with curated abstract covers.

### Cover rotation (confirmed-reachable URLs)

Pick randomly per page from this set:

```
https://www.notion.so/images/page-cover/gradients_2.png
https://www.notion.so/images/page-cover/gradients_3.png
https://www.notion.so/images/page-cover/gradients_5.png
https://www.notion.so/images/page-cover/gradients_8.png
https://www.notion.so/images/page-cover/gradients_10.jpg
https://www.notion.so/images/page-cover/gradients_11.jpg
https://www.notion.so/images/page-cover/met_william_morris_1875.jpg
https://www.notion.so/images/page-cover/woodcuts_4.jpg
https://www.notion.so/images/page-cover/solid_blue.png
```

Different cards getting different covers is fine — random per-page is the goal.

### How to apply

**At create time** — include the cover in the POST `/v1/pages` body:

```python
import random
COVERS = [...]  # the list above
body = {
    "parent": {"database_id": EVERGREEN_DB_ID},
    "cover": {"type": "external", "external": {"url": random.choice(COVERS)}},
    "properties": {...},
    "children": [...],
}
```

**Retro-fix** — PATCH `/v1/pages/<id>` with the same `cover` payload.

## 2. Verbatim quotes — paragraph blocks with straight `"..."`, NOT `quote` block type

Every verbatim quote in the post body is rendered as a **regular paragraph block** wrapping the text in straight ASCII quotation marks (`"..."`). Never use Notion's `quote` block type (the one with the vertical accent bar in the UI).

### Why

Notion silently transforms `quote`-type blocks server-side: the block is stored as a `paragraph` and the content is wrapped in **curly Unicode quotes** (`U+201C` / `U+201D`). The card looks fine in Notion, but copy-paste to X or Typefully drags those curly quotes through, which:

- Breaks visual consistency on X (X renders smart quotes inconsistently across web/iOS/Android)
- Forces a manual find-replace step before scheduling
- Risks getting flagged as low-quality by Typefully's preview comparison

Paragraph blocks with literal straight `"..."` survive Notion → clipboard → X drafter → published post intact.

### How to apply

```python
# ✅ Correct
{
    "object": "block", "type": "paragraph",
    "paragraph": {
        "rich_text": [{
            "type": "text",
            "text": {"content": '"He had to borrow money to pay rent."'}
        }]
    }
}

# ❌ Wrong — Notion will curly-quote the content
{
    "object": "block", "type": "quote",
    "quote": {"rich_text": [{"type": "text", "text": {"content": "..."}}]}
}
```

Applies to all 2–4 verbatim quotes in every Goku post body.

### Visual readability

The `"..."` marks themselves are sufficient visual signal that a passage is a quote — readers' eyes catch the marks. The vertical-bar styling of Notion's quote block is heavier visual noise that the card doesn't need.

## 3. Local clip path — render as code-styled plain text (Notion API blocks `file://` links)

Every sub-item post page has a Clip Spec section with a "Local clip path:" line. **The path is rendered as code-styled plain text, NOT as a hyperlink.** A previous version of this doc instructed using `file://` URLs; that approach is now known not to work and is documented here so no future agent re-introduces it.

### Required format

The clip path bullet is built via the Notion API as a `bulleted_list_item` block whose `rich_text` is two segments:

1. `"Local clip path: "` with `bold: true`
2. `"~/Desktop/goku-clips/<source>/<slug>.mp4"` with `code: true` (no `link` field)

Same shape for SRT:

1. `"Local SRT path: "` with `bold: true`
2. `"~/Desktop/goku-clips/<source>/<slug>.srt"` with `code: true` (no `link` field)

**Do not send markdown like `[text](file://...)`** via the MCP create-pages tool — Notion's markdown parser strips `file://` URLs, then auto-links the bare `.mp` prefix as `http://`, producing a broken `[<slug>.mp](http://<slug>.mp)4` artifact.

**Do not send rich_text with `link.url: "file:///..."`** via the raw Notion API — the endpoint returns `400 Invalid URL for link.`

### Why this is the right call

Two hard constraints from Notion as of May 2026:

1. **Markdown layer:** the MCP `notion-create-pages` tool's markdown parser does not preserve `file://` URLs. They get dropped and a broken `http://` auto-link is inserted instead.
2. **REST API layer:** `PATCH /v1/blocks/<id>` with a `rich_text` containing `link.url` starting with `file://` returns `"Invalid URL for link."` Notion only accepts `http://` and `https://` schemes.

Plain code-styled text dodges both. The user can copy the path with one click on the inline-code background, then run `open <path>` in Terminal (which reveals the file's parent folder in Finder), or paste the path into Notion's Cmd-K link dialog manually — the Notion **desktop app** accepts `file://` when typed by a human, just not when posted via API.

### Subfolder rule

Clips are grouped by source video in subfolders. Auto-derived from the slug's first segment (e.g. `baszucki-roblox-10m-vs-improbable` → folder `baszucki/`). Same speaker on a different show gets its own folder (e.g. `andreessen-senra/`, `andreessen-lex/`).

### Applies to

- All sub-item posts created by `scripts/notion_upload.py` (the local-path bullets in the Clip Spec section).
- Every Phase 2 sub-item created in `Evergreen Backlog`.
- The retro-fix path: any existing card with a broken `[<slug>.mp](http://<slug>.mp)4` artifact should be PATCHed to the plain code-styled rich_text shape above.

## Retro-fix script (reference)

If a previously-created card has the wrong cover or curly quotes:

- **Wrong cover:** PATCH `/v1/pages/<id>` with the random-gallery payload.
- **Curly quotes in paragraphs:** GET children, find paragraph blocks where `plain_text` contains `“` / `”` / `‘` / `’`, PATCH each with `rich_text` rebuilt using straight ASCII equivalents.
- **`quote`-type blocks (legacy):** for each one — append a new paragraph after it (`PATCH /v1/blocks/<parent>/children` with `after: <quote_id>` and a paragraph wrapping the content in straight `"..."`), then archive the original quote block (`PATCH /v1/blocks/<quote_id>` with `archived: true`).
