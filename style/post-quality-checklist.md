# Post Quality Checklist

Run this before delivering any draft. **Every box must check.** If any fails, rewrite before showing the user.

## Hook (15 words max)

- [ ] Format: `[Speaker] says [named actor] [violent verb] [named target] [specific anchor]`
- [ ] Reporting verb is exactly `says`. Not `just revealed`. Not `claims`. Not `argues`.
- [ ] **Violent verb is present** — `killed`, `crushed`, `lit on fire`, `broke`, `swallowed`, `wiped out`, `buried`, `gutted`, `flipped`. (See full list in `hook-recipe.md`.) **Reject hooks that use `built`, `created`, `started`, `worked on`, `helped`, `said`, `revealed`** — these describe instead of dramatize.
- [ ] Named actor (specific person/company/place, not "a founder" or "Big Pharma")
- [ ] Named target (the entity getting hit/changed/destroyed)
- [ ] Exactly one specific anchor — number, date, or visual detail (`$180M`, `September 1993`, `20 Jaguars`). Zero = vague. Three = list.
- [ ] No recency words anywhere: no `just`, `now`, `today`, `this week`, `breaking`, `recently`
- [ ] Credential prefix only if bare name is weak (`Dr.`, `Netscape founder`, `Sequoia's`)
- [ ] Word count 11–14 ideal, 15 max

## Body (240–260 words)

- [ ] **Counted, not estimated.** Actual word count is in the 240–260 range. (Slight under at 230 acceptable if cuts are clean and post lands.)
- [ ] **Sentence length varies deliberately.** Mix 4–6-word punches with 10–14-word narrative beats. Not all-fragments. Not all-long. A staccato post of 4-word fragments reads as unreadable.
- [ ] Every prose sentence ≤15 words. Quotes exempt. At most one sentence over 15 (used for the heaviest narrative beat — like the AOL/Athens setup).
- [ ] **Narrative arc is present** — setup → inciting moment → consequence cascade → reflection → open Q. Reader feels they're walking through a story, not reading a list of claims. **Avoid the insight-stack pattern** (claim → quote → claim → quote).
- [ ] **Stay close to the source. No author voiceover on top of the story.** Every body sentence does one of: quotes the speaker, states a specific fact the speaker named, bridges the narrative (Then hinge / speaker stake / transition between quotes), or explains the etymology of a named concept the source introduced. **Audit-cut pattern:** generic author observations like *"The boring stuff compounds. The exciting stuff usually doesn't."* / *"That's a moat most companies would defend."* / *"Most platforms compete for time."* — interpretive voiceover laid *on top of* the story, not insight derived *from* it. Insight should land through the cascade and the speaker's reflective quote.
- [ ] 2–4 direct verbatim quotes from the transcript.
- [ ] Reported speech only. No first-person voice in body. No "I think", no "in my view".
- [ ] **Quote attribution varies — never the same shape twice in a row.** Rotate through: no attribution at all (quote attaches after a setup sentence), character-stake lead (*"Andreessen, who was building Mosaic at the time, watched it happen."*), temporal/situational lead (*"Andreessen, looking back:"*), bare name + colon (max 1× per post), inline quote inside prose. **Audit-trigger pattern: stacked *"[Speaker], on X:"* labels.** Three of those in a row turns the post into a transcript heading. If you find yourself reaching for it three times, rewrite the surrounding prose so quotes attach naturally.
- [ ] **Bullet blocks allowed when the content is list-shaped.** 3+ parallel items, 3–6 words each, fragments. Use when the list wants to breathe visually. One bullet block per post max. Default is still inline parallel triplets unless the rhythm calls for bullets.
- [ ] No tabloid adjectives: no `shocking`, `unbelievable`, `jaw-dropping`, `insane`, `crazy`, `mind-blowing`.
- [ ] No recency words anywhere in the body.
- [ ] **Body deploys 2–4 named techniques from `body-techniques.md`** (number cascade, dialogue exchange, closing paradox, speaker stake in prose, before/then, named-concept boldface, visual detail trio, end-on-verbatim, hedge preservation). Fewer than 2 = summary, more than 5 = overstuffed.
- [ ] **Required narrative moves — at least 3 of 5 present** (per master-prompt.md May 2026 update):
  - [ ] (1) Named concept is **bolded** on first use (one per post max). Skip if post has no named concept.
  - [ ] (2) Speaker stake woven into prose, not a credential paragraph (e.g. *"Andreessen, who was building Mosaic at the time, watched it happen."*)
  - [ ] (3) Body ends on a **reflective verbatim quote where the speaker takes both sides** (pro/con, win/cost, gratitude/regret), not author-voice reflection
  - [ ] (4) **"Then" hinge sentence** — single-sentence pivot, on its own line, with whitespace around it (*"Then America Online bought a connection to it."*)
  - [ ] (5) **Memorable reframe in the setup**, not just description (*"They were the smartest two million people in the world."* vs. *"The internet had 2M users."*)
- [ ] **Andreessen-grade polish rules** (per master-prompt.md v3 update — gradient: critical vs nice-to-have):

  **Critical (apply whenever the post supports it):**
  - [ ] (P1) Every prose verb is specific and active — no filler *had / got / was / built / made / did* unless intentional. Active verbs do the lifting (*pumped, swallowed, layered, watched*).
  - [ ] (P5) **One hero, many witnesses.** Other named entities (host included) populate the speaker's world without getting their own narrative beats. **Audit-trigger:** *"Then [host] asked the question. / [host]: '...'"* — absorb host's question into the speaker's response instead.
  - [ ] (P6) No qualifier creep on the central claim — drop *"according to X"* / *"X thinks"* / *"X believes"* / *"in X's view"*. The hook's *"says"* covers it.
  - [ ] (P7) Every prose sentence carries a concrete anchor — named entity, number, date, or sensory detail. Cut generic claims (*"the trajectory was clear"* / *"the market expanded"*) or replace with specifics.
  - [ ] (P8) Past tense throughout the narrative spine when the source is dated. Present tense reserved for speaker quotes and present-day state of still-existing entities.

  **Nice-to-have (deploy when the post genuinely earns it; skip if forcing it would feel artificial):**
  - [ ] (P2) If post has a strong named concept, the concept can echo at multiple scales (mechanism → naming → live noun). Don't force this if the post doesn't have a dominant named term.
  - [ ] (P3) If the rupture has a permanent aftermath worth naming, deploy the *"After X, Y"* consequence marker on its own line. Skip if the rupture closes itself.
  - [ ] (P4) If the post needs a deliberate slowdown to enrich a named concept's mechanism, the one allowed >15-word sentence can carry it. Otherwise, don't use the exception at all.
- [ ] **No credential paragraph at body open** (use technique 4 — speaker stake in prose — instead).
- [ ] Body lands on a sharp line — verbatim quote, paradox, or stark single-sentence statement that earns the engagement Q. **Never a soft summary or "what this means is…" line.**

## Closer (after body, in this order)

Order on the `experimental-hemingway` branch: **Body One-Liner Close → P.S. (Product CTA) → Brand CTA → Attribution.** Engagement Q is deprecated — the body itself ends on a reflective one-liner. P.S. now comes BEFORE Brand CTA.

- [ ] **Body One-Liner Close**: the body's last line is a reflective punch on its own line (e.g. *"That was the war Machiavelli watched."*). No question prompt. See `closer-template.md` §1.
- [ ] **P.S. — fixed drop-in wording, 3 short paragraphs with blank lines between (Product CTA comes BEFORE Brand CTA).** Verbatim per `closer-template.md`. **No personalization, no theme-tie, no agitation.** The body did the narrative work; the P.S. is just the clean product handoff. Order: offer → pain/desire → DM mechanic. Same on every post:
  ```
  P.S. I made a full playbook breaking down the timeless decision-making mental models used by history's greatest thinkers.

  So if you want to stop overthinking, control chaos, and navigate any decision with the clarity...

  Comment "models" and follow @GeniusGTX so I can DM you a copy.
  ```
- [ ] **Brand CTA**: VERBATIM as in `closer-template.md` ("If you're new here, follow @GeniusGTX for content on the greatest minds in economics, psychology, and history."). Not paraphrased.
- [ ] **Whitespace audit on the entire post.** One sentence per line is the default. Blank lines between every paragraph. The post should look airy on the page, not like a chunk. The reader's eyes should never hit a wall of text — especially in the closer.
- [ ] **Attribution**: format `— [Name] ( @handle ), [credential], on [Host] ( @host_handle ) [Show]`. **Spaces inside parentheses around every @handle** so X auto-tags render.

## Source fidelity

- [ ] Every claim in the body traces to the transcript (or is reported speech you can defend).
- [ ] Every direct quote is verbatim from the source — character-for-character.
- [ ] Every named person/company/place mentioned is actually named by the speaker (or is your reasonable inference, marked clearly).
- [ ] No assertions in your own voice that aren't backed by the source.
- [ ] If the speaker hedges ("I think it was Adeo Ressi"), preserve the hedge in your prose.

## Clip spec

- [ ] Clip range covers every quoted line in the post body
- [ ] Start cue is verbatim from the transcript and passes the standalone-hook test (see `clip-selection.md`)
- [ ] End cue is verbatim and lands with finality (sharp line, punchline, quote, stark statement)
- [ ] Clip length 2:00–4:00 (sweet spot 2:30–3:30)
- [ ] Slug for the local mp4 follows the naming convention (lowercase, hyphens, derived from post title)

## Phase 2 readiness

- [ ] **Target database is `Evergreen Backlog`** (Notion). Sub-item is created there, parented to the source video page.
- [ ] Notion sub-item title matches the post hook claim (or a short distillation)
- [ ] Topic Tags set (1–4 from the schema)
- [ ] Parent video relation linked
- [ ] Local clip path in body rendered via the Notion API as a `bulleted_list_item` with `rich_text` of `"Local clip path: "` (bold) + `"~/Desktop/AI Agents/clips/<source>/<slug>.mp4"` (code-styled, NO link annotation). Do NOT use markdown `[text](file://...)` syntax — Notion's parser strips it and inserts a broken `http://` auto-link. Do NOT set a `file://` link annotation — the REST API returns `"Invalid URL for link."` See `notion-card-rendering.md` §3.
- [ ] **Cover image set** to a random pick from `config/notion-schema.json:cover_image_recommendations` (both parent video page AND sub-item). Not a YouTube thumbnail. See `notion-card-rendering.md`.
- [ ] **Verbatim quotes rendered as `paragraph` blocks** with straight `"..."` ASCII marks. Never `quote` block type — Notion curly-quotes the content and breaks copy-paste to X. See `notion-card-rendering.md`.

## If the user has standing rules from past sessions

Always check `~/.claude/projects/.../memory/feedback_*` for the latest preferences. If a rule there contradicts this checklist, the memory rule wins (it's the more recent decision).

Currently active feedback rules (May 2026):

- **Engagement Q must be open + story-rooted**, NOT a formulaic A/B binary. (Updated May 2026 — supersedes the old "simple binary" rule.)
- **Narrative arc required** — setup → inciting moment → consequence cascade → reflection → open Q. The Andreessen "Eternal September" post is the canonical example. (Added May 2026.)
- **Sentence length varies deliberately** — mix short punches with longer narrative beats. Not all-fragments. (Added May 2026.)
- **P.S. has personalized PAS para 1 + fixed playbook plug** (Feynman/Munger/Musk + 90+ tools + 5,000+ founders/investors). Old "free toolkit / 113 five-star reviews" wording deprecated. (Updated May 2026.)
- **Clip start cue must match the audio verbatim** — including any filler words ("Um", "you know") that begin the spoken phrase. Don't cherry-pick the cleanest version of the line. (Added May 2026.)
- No recency words in posts
- Word count target 240–260
- Spaced handles in attribution
- Manual drag-drop or parallel API attach for Typefully (user-controlled)
- Slug naming for clip files
- Pre-cut clip in parallel with draft delivery
- Clip output to `~/Desktop/AI Agents/clips/<source>/` — clips grouped by source video in subfolders for Finder browsability. Subfolder auto-derived from slug's first segment (`baszucki/`, `andreessen/`, `naval/`, `dell/`, `musk/`).

If any of these conflict with what this checklist says, do what the memory rule says — it's the more recent decision.
