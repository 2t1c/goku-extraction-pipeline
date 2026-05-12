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

## 3. Local clip path — render as a `file://` hyperlink that opens in Finder

Every sub-item post page has a Clip Spec section ending in a "Local clip path:" line. **The path must be rendered as a clickable hyperlink that opens the file (and its enclosing folder) in macOS.** Clicking it from the Notion desktop app reveals the clip in Finder.

### Required format

```
- **Local clip path:** [~/Desktop/AI Agents/clips/<slug>.mp4](file:///Users/toantruong/Desktop/AI%20Agents/clips/<slug>.mp4)
```

Two parts:

- **Visible text:** the human-readable `~/`-rooted path. Easy to read in the card.
- **Underlying URL:** `file:///` + absolute path with **`%20`** in place of every space (URL-encoding is required for spaces, otherwise Notion silently breaks the link).

### Why URL-encoding matters

The folder name is `AI Agents` (with a space). Raw spaces in a `file://` URL break it in Notion. URL-encoded `AI%20Agents` is the only form that survives the Notion editor and clicks correctly.

```
✅ file:///Users/toantruong/Desktop/AI%20Agents/clips/dell-bus-past-rice-stock-ticker.mp4
❌ file:///Users/toantruong/Desktop/AI Agents/clips/dell-bus-past-rice-stock-ticker.mp4
```

### What NOT to do

- ❌ **Bare path** (e.g. `~/Desktop/AI Agents/clips/<slug>.mp4` with no link). Notion auto-links the `.mp` prefix as an `http://` URL, producing a broken `[<slug>.mp](http://<slug>.mp)4` artifact that points to nowhere.
- ❌ **Backslash-escaped tilde** (`\~/Desktop/...`) — the backslash leaks into the rendered text.
- ❌ **Without `file:///`** — without the scheme, Notion treats it as plain text.

### Click behavior

Clicking the link in the Notion desktop app on macOS:
1. Hands the `file://` URL to the OS
2. macOS opens the `.mp4` in the default video player (QuickTime) AND/OR can be configured to reveal in Finder
3. To always reveal in Finder, the user can also link the parent folder separately as a secondary `[📁 Open clips folder](file:///Users/toantruong/Desktop/AI%20Agents/clips/)` line.

### Applies to

- All sub-item posts created by `scripts/notion_upload.py` (the local-path line in the Clip Spec section).
- Every Phase 2 sub-item created in `Evergreen Backlog`.
- The retro-fix path below for any existing cards with broken bare-path renders.

## Retro-fix script (reference)

If a previously-created card has the wrong cover or curly quotes:

- **Wrong cover:** PATCH `/v1/pages/<id>` with the random-gallery payload.
- **Curly quotes in paragraphs:** GET children, find paragraph blocks where `plain_text` contains `“` / `”` / `‘` / `’`, PATCH each with `rich_text` rebuilt using straight ASCII equivalents.
- **`quote`-type blocks (legacy):** for each one — append a new paragraph after it (`PATCH /v1/blocks/<parent>/children` with `after: <quote_id>` and a paragraph wrapping the content in straight `"..."`), then archive the original quote block (`PATCH /v1/blocks/<quote_id>` with `archived: true`).
