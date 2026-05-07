# Goku Master Prompt — current rules (May 2026)

The Goku format is the foundation. **The rules below are the live overrides** — when something here conflicts with an older canonical Goku doc, this file wins.

## The viral formula

```
AUTHORITY CLAIM → SHOCKING FACT → MECHANISM/STORY →
SPECIFIC EVIDENCE → MASS IMPLICATION → QUIET CONSPIRACY/SUPPRESSION → CTA
```

## Hook format

```
[Speaker] says [named actor] [violent verb] [named target] [specific anchor].
```

- **≤15 words.** Hard ceiling. Aim 11–14.
- **Verb is `says`. Period.** Not `just revealed`, not `recently said`, not `claims`, not `argues`. Source podcasts are dated; recency words read as dishonest. (See `no-recency-words.md`.)
- **Violent verb is non-negotiable.** `killed`, `crushed`, `lit on fire`, `broke`, `swallowed`, `wiped out`, `buried`, `gutted`, `flipped`. **Bland verbs (`built`, `created`, `started`, `worked on`) are not Goku hooks** — they describe instead of dramatize. Full list + worked transformations in `hook-recipe.md`.
- **Named actor + named target.** Both must be specific entities (person, company, place). Not "a founder" or "Big Pharma" — `Elon`, `AOL`, `Hollywood`.
- **One specific anchor.** Number, date, or visual detail (`$180 million`, `September 1993`, `20 identical Jaguars`). Exactly one — zero is vague, three is a list.
- Credential prefix only if the bare name is weak (`Dr.`, `Netscape founder`, `Sequoia's`). Pick the shortest phrase that establishes authority.

**Read `hook-recipe.md` before drafting.** Bland-vs-Goku transformations live there.

## Body rules

- **Word count: 240–260.** Aim for 245–255. Don't deliver shorter than 220 — denser posts perform better. Don't pad to hit the ceiling — cut weak beats first. (See `word-count.md`.)
- **Sentence length: vary deliberately.** Hard cap is 15 words on prose sentences; quotes exempt. At most one sentence over 15. **Mix lengths on purpose** — 5-word punches alongside 10–14-word narrative beats. Three-fragment parallel triplets ("No advertising. No commerce. No spam.") are powerful when deployed sparingly as deliberate beats — never as default rhythm. A post that is all 4-word fragments reads as staccato and unreadable.
- **Narrative arc, not insight stack.** Strong posts walk the reader through: setup → inciting moment → consequence cascade → reflection → open question. The reader feels they're learning a story, not getting hit with a list of claims. **Avoid the insight-stack pattern** (claim → quote → claim → quote → claim → quote) — that reads as a summary, not a story. See `body-techniques.md` for arc structures.
- **Reported speech only.** No first-person voice in the body except verbatim quotes. "Andreessen says…", "Per Andreessen:", "In his words:".
- **No tabloid adjectives.** Banned: shocking, unbelievable, jaw-dropping, mind-blowing, insane, crazy. Let the facts sound sensational on their own.
- **No recency words.** No "just", "now", "today", "recently", "this week" framing the claim as breaking. Past-tense reportage when the source is dated.
- **2–4 verbatim quotes per post.** Quotes are exempt from the 15-word cap. Strongest move: end the body with a direct quote OR a tight reflection that earns the engagement Q.
- **Quote attribution: vary the technique. Don't tag every quote the same way.** The Andreessen "Eternal September" post is the canonical reference for how to mix attribution naturally. Patterns to rotate through:
  - **No attribution at all** when the speaker is established and the quote follows a setup sentence that does the work. *"Andreessen says it felt like Athens in 500 BC."* → next line, the quote attaches directly: *"'The most pure, clean, intellectual, vibrant space' since the Greeks."*
  - **Character stake as attribution.** *"Andreessen, who was building Mosaic at the time, watched it happen."* → next line, the quote: *"'That's the day the internet changed.'"* (Doubles as narrative, not just labeling.)
  - **Temporal/situational lead.** *"Andreessen, looking back:"* / *"Twenty years later:"* / *"After the breach:"* — leads that frame *when* or *under what conditions*, not just *that the speaker is about to talk*.
  - **Bare name + colon, used 1× per post max.** *"Baszucki:"* alone is fine **once**. Stacking two of these reads as a transcript heading, not a story. If you find yourself reaching for it three times in a single post, rewrite the surrounding prose so quotes attach naturally.
  - **Inline quote tucked into prose.** *"He saw the obvious problem early — 'we had no flow control anywhere in the economy' — and the team killed the launch within a week."* (Quote inside a longer narrative sentence.)
  
  **The bad pattern to audit:** stacking *"X, on Y:"* labels (e.g., *"Baszucki, on what they built:"* → quote → *"Baszucki, on the answer:"* → quote → *"Baszucki, looking back:"* → quote). Three of those in a row turns the post into a transcript. Use at most one *"X, on Y:"* form per post; for the rest, use the other patterns above or attach the quote directly.

- **Bullet blocks are allowed when the content is genuinely list-shaped.** A 3+ item parallel block (technical components, a list of named entities, a cascade of specifics) can render as a bulleted block when that's the cleanest way to land the rhythm. Default is still inline parallel triplets ("No advertising. No commerce. No spam."), but don't avoid bullets if the list wants to breathe more visually. One bullet block per post max.

## Andreessen-grade polish rules (May 2026 update v3)

Eight techniques the canonical Andreessen "Eternal September" post deploys that are now required when applicable. **These are the difference between "good narrative post" and "the kind of post people screenshot."**

- **(P1) Verb specificity audit.** Every prose verb should be doing work. The Andreessen post lifts on active, specific verbs: *"AOL **pumped** two million normal people directly onto the internet"* / *"swallowed by the next two million"* / *"watched it happen."* Audit drafts for *had / got / was / is / built / made / did* — these are filler. Replace with verbs that carry meaning. *"Roblox built the safety stack from week 3"* → *"Roblox **layered** the safety stack from week 3 forward."*

- **(P2) Echo the named concept across three scales of meaning.** When a post bolds a named concept (per move #1), the concept should also appear twice more in different forms — building progressively. The Andreessen post moves: setup of the mechanism (*"Every September, when the new freshmen got their college email accounts, the discussion forums would briefly drop in quality"*) → naming (*"It became known as **Eternal September**"*) → noun the reader now owns (*"the September never ended"*). Three scales: mechanism → name → live concept. Posts that bold once and never echo feel half-built.

- **(P3) The "after X, Y" mirror to the "Then" hinge.** Sometimes a post needs to mark the *consequence*, not just the trigger. The Andreessen post pairs *"Then America Online bought a connection to it."* (trigger) with *"After AOL connected, the September never ended."* (consequence). Both sit on their own lines with whitespace. When the rupture has a permanent aftermath worth naming, deploy the consequence marker as a sister to the "Then" hinge.

- **(P4) Earn one mid-post explainer beat.** The single >15-word sentence allowed per post should be the deliberate *slowdown* that enriches the named concept's mechanism. The Andreessen post's 28-word sentence ("Pre-1993 internet veterans had a phrase. Every September…") is the *only* place the post breathes — and it teaches the reader the etymology of *Eternal September*. Wasting the one allowed exception on a generic claim or a stat sentence is leaving the technique on the table.

- **(P5) One hero, many witnesses.** The post focuses on one speaker's perspective. Other named entities are *actors in that story*, not separate narrative perspectives. AOL, Mosaic, freshmen — they populate Andreessen's world; they don't get their own beats. **Audit-trigger pattern:** giving the host their own narrative line (*"Then Senra asked the question. / Senra: '...'"*) shares narrative weight and breaks the spell. Stronger version absorbs the host's question into the speaker's response: *"When asked if Roblox would license the safety stack, Baszucki said yes."* The host vanishes into the prose; the speaker keeps the spotlight.

- **(P6) No qualifiers on the central claim.** Once the *"X says Y"* hook establishes the speaker as the source, the body operates as documented narrative. The Andreessen post asserts *"AOL killed the early internet"* as fact — no *"according to Andreessen"* / *"he believes"* / *"in his view"* hedges. The single "says" in the hook covers everything below it. Drop qualifier creep: *"Baszucki thinks"* / *"in Baszucki's read"* / *"his frame is"* — these multiply confidence costs without adding accuracy. Trust the hook's "says."

- **(P7) Concrete sensory anchor per sentence.** Audit any sentence that doesn't carry a named entity, a number, a date, or a sensory detail. The Andreessen post has zero generic claims — every sentence anchors to *Athens in 500 BC*, *September 1993*, *five billion*, *Mosaic*, *the new freshmen*, *the discussion forums*. Replace generic claims (*"The trajectory was clear"* / *"The team grew quickly"* / *"The market expanded"*) with specifics, or delete them.

- **(P8) Past tense control.** When the source is dated (a podcast from last month or last year), keep the body in past tense even for ongoing realities. *"Then America Online bought a connection to it."* (not *"buys"* or *"has bought"*). Past tense puts the reader in the historical frame; present tense pulls the post into "current events" mode and breaks the storytelling spell. **Exception:** speaker quotes can be present tense ("X says…"), and statements about the present-day state of a still-existing entity can be present tense (*"Roblox runs at 13 billion hours per month"*) — but the *narrative spine* of the post stays past.

## Required narrative moves (May 2026 update)

These five moves came out of audit against the Andreessen "Eternal September" canonical post. **Strong posts deploy at least 3 of these; weak posts skip them all.**

- **(1) Bold the named concept on first use.** Every post that has a shareable handle (`**Eternal September**`, `**Builder's Club**`, `**perpetual motion machine**`) gets it bolded — one per post max. The bolded term is what someone Googles afterward, what gets quoted in screenshots, what carries the post into other conversations. Posts without a named concept don't get a bold; don't invent one to hit the quota.
- **(2) Speaker stake in prose, not a credential paragraph.** The speaker's authority should be woven into the narrative at the moment it matters: *"Andreessen, who was building Mosaic at the time, watched it happen."* / *"Baszucki, who'd been coding world simulations since the Apple II, knew which game he was actually building."* This replaces standalone "Marc Andreessen, co-founder of Netscape, said..." setups. **Required when the speaker's authority is load-bearing for the claim.**
- **(3) End the body on a reflective verbatim quote where the speaker takes both sides.** The strongest body endings have the speaker himself acknowledge the tension — pro/con, win/cost, regret/gratitude. *"I'm pro that. I'm glad that happened. But the pro and the con of that is..."* The reader gets the post's central tension delivered in the speaker's own voice. **Then** the engagement Q invites them in. Author-voice closing reflections are weaker than speaker-voice ambivalence.
- **(4) The "Then" hinge — single-sentence pivot, on its own line.** Every story has the moment when the world changes. Mark it visually: *"Then America Online bought a connection to it."* / *"Then he ignored that instinct."* / *"Then one night, a vision arrived."* One sentence, one line, sandwiched in white space. The post pivots on it. Don't bury this hinge inside a paragraph.
- **(5) Memorable reframe in the setup, not just description.** The opening should reframe the world the reader is about to walk into, not just describe it. *"They were the smartest two million people in the world."* (vs. "The internet had two million users in 1993.") *"Roblox's first 1,500 users were the entire seed crystal of a graph that today connects 70 million daily players."* (vs. "Roblox started with 1,500 users.") The reframe is the line that makes the rest of the post inevitable.

## Body toolkit (use what fits, skip what doesn't)

The named techniques live in `body-techniques.md` with worked examples. Quick index:

- **Number cascade** — `2M → 2M → 20M → 5B`, single beat compresses scale.
- **Verbatim dialogue exchange** — 2–4 short quotes back-to-back as theatrical exchange.
- **Closing paradox** — `wrong about the rockets, right about the fire`.
- **Speaker stake in prose** — `Andreessen, who was building Mosaic at the time, watched it happen.` (Replaces credential paragraphs.)
- **Before / then** — two-paragraph hinge on `Then`, `Until`, `One day`.
- **Named-concept boldface** — `**Eternal September**` on first use. One bold per post max.
- **Visual detail trio** — three concrete sensory specifics (brands, counts, identifiers).
- **End-on-verbatim-quote** — let the speaker close.
- **Hedge preservation** — if the source hedges, the post hedges.

Plus the universal building blocks:

- **Mechanism explanation** — 2–4 sentences naming a system, law, or process (Kleiber's Law, Eternal September, "managerialism").
- **Bullet blocks** — 3–6 word fragments, used when there are 3+ parallel items.
- **Direct quotes** — 2–4 per post. Strongest are named concepts, accusations, predictions.
- **Suppression layer** — name the institution that benefits from silence. Use when source explicitly covers it.
- **Stacked credibility** — second source, court ruling, peer study, government data.

Strong posts deploy 3–4 techniques. Fewer than 2 reads as a summary. More than 5 feels overstuffed.

## Closer (4 parts, in order)

1. **Engagement Question** — simple binary opinion question (e.g. *"Genius — or ruthless?"*). See `closer-template.md`.
2. **Brand CTA (verbatim).**
3. **P.S. Product CTA (verbatim).**
4. **Attribution** — `— [Name] ( @handle ), [credential], on [Host] ( @host_handle ) [Show]`. **Spaces inside parentheses around handles** so X auto-tags render.

(See `closer-template.md` for the verbatim wording of items 2–3 and the attribution format.)

## Topic tier hierarchy

- **Tier 1 (500K+ potential):** tech/government conspiracy affecting health; mainstream belief being proven wrong; named-Elon angles for @GeniusGTX.
- **Tier 2 (100K–500K):** cutting-edge science; named insiders who got it wrong; paradigm-break corporate stories.
- **Tier 3 (50K–150K):** quirky historical facts; founder origin stories; cultural pattern posts.

## Virality stress test (run before delivering)

- [ ] Hook: `[Speaker] says [actor] [VIOLENT VERB] [target] [anchor]`, ≤15 words
- [ ] Hook verb is from the violent-verb list (`killed`, `crushed`, `lit on fire`, etc.) — **not** `built`, `created`, `said`, `revealed`
- [ ] Hook has named actor AND named target (both specific entities)
- [ ] Hook has exactly one specific anchor (number, date, or visual detail)
- [ ] Hook has no recency words ("just", "now", "today", "recently")
- [ ] Body: 240–250 words (count it, don't estimate)
- [ ] Every prose sentence ≤15 words (at most one exception)
- [ ] 2–4 direct verbatim quotes
- [ ] Reported speech only — no first-person, no tabloid adjectives
- [ ] Body deploys 2–4 named techniques from `body-techniques.md`
- [ ] Body ends on a verbatim quote, paradox, or sharp single-sentence statement (never a soft summary)
- [ ] Engagement Q is a simple binary, not "where in your life"
- [ ] Brand CTA + P.S. Product CTA verbatim
- [ ] Attribution has spaces inside parentheses on handles

If any box is unchecked, rewrite before delivering.

## Reading order for new agents

1. This file (you are here).
2. `hook-recipe.md` — the violent-verb hook formula. **Read before drafting any hook.**
3. `body-techniques.md` — number cascades, dialogue exchanges, closing paradoxes, speaker stake.
4. `closer-template.md` — closer details.
5. `word-count.md` — how to hit 240–250 without padding.
6. `no-recency-words.md` — the ban list and replacements.
7. `clip-selection.md` — clip pick after you've drafted.
8. `extraction-workflow.md` — Phase 1 / Phase 2 mechanics.
9. `examples/andreessen-interview/extracted-posts/` — worked examples of finished posts.
