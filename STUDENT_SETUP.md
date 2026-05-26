# Student Setup — make this pipeline yours

This branch is the **student edition** of the GeniusGTX long-form pipeline.

The *taste* (hook recipe, body discipline, topic ranking, clip selection) stays GeniusGTX. That's the part you came here to learn — keep it locked. What you change is the surface: your handle, your product, and the niche you point the ranking rubric at.

Three things to swap before you run the pipeline:

1. **Your handle** — wherever the brand CTA says `@GeniusGTX`
2. **Your product CTA** — the P.S. that drives the click
3. **Your niche taste** — which kinds of ideas you elevate inside the same scoring rubric

Everything else (`master-prompt.md`, `hook-recipe.md`, `body-techniques.md`, `word-count.md`, `clip-selection.md`, the Andreessen worked examples) is the standard. Don't fork it until you've shipped 20–30 posts.

---

## 1. Your handle

Open `style/closer-template.md` and search for `{{BRAND_HANDLE}}`. Replace with your handle (with the `@`).

The line lives in two places — the Brand CTA block and the worked example at the bottom.

```
If you're new here, follow {{BRAND_HANDLE}} for content on {{BRAND_DESCRIPTION}}.
```

Fill in `{{BRAND_DESCRIPTION}}` with one short noun phrase that describes what your page is about. Examples:

- *content on the greatest minds in economics, psychology, and history* (GeniusGTX)
- *the founders, operators, and frameworks that build $1B companies*
- *clear thinking about money, markets, and the stories behind them*
- *primary-source history for builders who don't have time to read the books*

One sentence. Don't try to be clever — clean signal beats clever copy.

## 2. Your product CTA

Open `style/closer-template.md` and pick **one of the two Product CTA mechanics**:

- **Option A — comment-to-DM** (use when the product is paid). You gate the link behind a comment so you can qualify intent and DM the right link.
- **Option B — direct URL** (use when the product is free or the funnel is wide). You drop the URL in the P.S. and let people click.

Both blocks have placeholders:

- `{{PRODUCT_NAME}}` — the name of the thing (e.g. *Incentives*, *Mental Models Playbook*, *Cold Email Vault*)
- `{{PRODUCT_DESCRIPTION}}` — one line on what it is (e.g. *a short book on how to spot hidden incentives*)
- `{{PRODUCT_SOCIAL_PROOF}}` — downloads / reviews / customers, **only if you have real numbers**. If you don't, delete the line. Made-up social proof corrodes trust.
- `{{PRODUCT_URL}}` — the Gumroad / Stripe / landing-page URL (Option B only)
- `{{DM_KEYWORD}}` — the comment trigger (Option A only). Pick a word that's short, easy to type, and tied to the product (`INCENTIVES`, `PLAYBOOK`, `VAULT`)

Don't have a product yet? Use Option B with `{{PRODUCT_URL}}` pointing to your newsletter signup or a free PDF you wrote. The P.S. slot is still doing work even when the product is free — it's training your audience that clicks lead somewhere useful.

## 3. Your niche taste

The 6-criterion topic ranking in `style/topic-ranking.md` is the GeniusGTX taste filter — contrarianism, specificity, mechanism, takeaway, villain, behavior attack. **Don't change the criteria.** They're what makes a Goku post a Goku post.

What you change is **the audience suspicion** the scoring is aimed at. GeniusGTX scores against the founder/investor/curious-operator gut. If your page is about:

- **Health** → score against "the food pyramid lied / my doctor is wrong / sugar is the villain"
- **Money** → score against "the index-fund story is a Wall Street trick / boomers got handed the asset / inflation is theft"
- **History** → score against "the textbook version is sanitized / the loser's version was right / the institutions buried this"
- **Tech** → score against "the consumer product is a surveillance trap / open source is being killed / the platform tax is a heist"

Open `style/topic-ranking.md`, find criterion 1 ("Belief-confirming contrarianism") and criterion 5 ("Conspiracy / suppression layer"). Edit the examples in those two sections to match your audience's gut. Leave the structure intact.

Optional: add a `style/niche-anchors.md` file with 10–20 named entities your audience cares about (the equivalent of GeniusGTX's *Elon, Andreessen, Munger, Andreessen, Naval, Baszucki*). The pipeline will surface ideas involving those names first.

---

## After you've changed the three things

Run the rest of the install from `INSTALL.md`:

1. Notion integration → `.env`
2. Typefully API key → `.env`
3. yt-dlp + ffmpeg
4. Verify with the test command in INSTALL.md §5

Then point an AI agent (Claude Code, Hermes, your own) at `SKILL.md` and give it a YouTube URL + transcript. Your first post should be in the queue inside 20 minutes.

## What NOT to change (for at least your first 30 posts)

- `style/master-prompt.md` — the rules. Earned over thousands of posts.
- `style/hook-recipe.md` — violent-verb hook formula
- `style/word-count.md` — 240–260 word body discipline
- `style/no-recency-words.md` — the ban list
- `style/body-techniques.md` — the named moves (P1–P8, the five required moves)
- `style/clip-selection.md` — standalone-hook rule for clip starts
- `style/post-quality-checklist.md` — the pre-ship audit

Ship 30 posts in the strict format. Then — and only then — start adapting.
