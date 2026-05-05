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
- [ ] 2–4 direct verbatim quotes from the transcript.
- [ ] Reported speech only. No first-person voice in body. No "I think", no "in my view".
- [ ] **Speaker connectors used 1–2 times max** ("Naval continues:", "Then Baszucki drops the historical context.", "[Speaker], looking back:"). Used sparingly to weave quotes into the narrative — not as default rhythm.
- [ ] No tabloid adjectives: no `shocking`, `unbelievable`, `jaw-dropping`, `insane`, `crazy`, `mind-blowing`.
- [ ] No recency words anywhere in the body.
- [ ] If bullets are used: 3+ parallel items, 3–6 words each, sentence fragments.
- [ ] **Body deploys 2–4 named techniques from `body-techniques.md`** (number cascade, dialogue exchange, closing paradox, speaker stake in prose, before/then, named-concept boldface, visual detail trio, end-on-verbatim, hedge preservation). Fewer than 2 = summary, more than 5 = overstuffed.
- [ ] **No credential paragraph at body open** (use technique 4 — speaker stake in prose — instead).
- [ ] Body lands on a sharp line — verbatim quote, paradox, or stark single-sentence statement that earns the engagement Q. **Never a soft summary or "what this means is…" line.**

## Closer (after body, in this order)

- [ ] **Engagement Q**: open natural question rooted in the post's specific tension, ≤16 words. **Not a formulaic A/B binary** ("Capital or discipline?", "Rent or own?") — those read as button-presses. The Q should invite the reader to apply the post's tension to their own situation. (See `closer-template.md` for examples.)
- [ ] **Brand CTA**: VERBATIM as in `closer-template.md` ("If you're new here, @GeniusGTX is a gallery..."). Not paraphrased.
- [ ] **P.S. — PAS para 1 is personalized**: opens the wound the post just exposed in 2 short sentences (≤45 words total), tied to the post's central tension.
- [ ] **P.S. — playbook plug paragraph + closer line are verbatim** as in `closer-template.md` ("I've made a free playbook... Feynman, Munger, and Musk... 90+ cognitive tools, trusted by 5,000+ founders and investors. / Grab your copy: [URL]").
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
- [ ] Local clip path in body for manual fallback: `~/Desktop/AI Agents/clips/<slug>.mp4`
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
- Clip output to `~/Desktop/AI Agents/clips/`

If any of these conflict with what this checklist says, do what the memory rule says — it's the more recent decision.
