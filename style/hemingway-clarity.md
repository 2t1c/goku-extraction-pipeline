# Hemingway-Grade Clarity — experimental Hemingway branch (May 2026)

This file codifies the readability rules for posts written on the `experimental-hemingway` branch.

## The target

**6–7th grade reading level.** Not 5th grade — that flattens the brand. Not 9–10th grade — that's where the un-edited drafts naturally land and feel academic. The Andreessen "Eternal September" canonical post sits at ~6th grade; that's the bar.

## Why we're tightening

@GeniusGTX is a gallery for the greatest minds in economics, psychology, and history. The audience signed up expecting **smart material delivered clearly** — not BuzzFeed prose, not academic prose. Hemingway-grade clarity is the meeting point:

- The intellectual material stays sophisticated.
- The prose stops fighting the reader.
- Load-bearing named concepts (`Eternal September`, `political science`, `Builder's Club`) keep their place.
- Latinate vocabulary that earns nothing gets cut.

## The 5 tactical rules

Apply these on every body draft, in order. Run an audit pass after the first draft is written.

### 1. Plain Anglo-Saxon verbs over Latinate ones

The verb is the smallest unit doing the most readability work. Anglo-Saxon verbs are short, concrete, and physical. Latinate verbs feel academic.

| Latinate (cut) | Anglo-Saxon (use) |
|---|---|
| commenced | started, began |
| eliminated | killed, wiped out |
| terminated | cut off, ended |
| manufactured | made, built |
| utilized | used |
| facilitated | helped, made possible |
| demonstrated | showed |
| identified | found, named |
| proposed | called it, suggested |
| executed | killed |
| acquired | bought, got |
| constructed | built |
| revealed | showed, said |
| recalled | said, remembered |
| explained | said, showed |

**Worked transformation:**

❌ `He proposes what we would think of as political science.`
- `proposes` is Latinate. Reads academic.

✅ `He calls it **political science**.`
- 5 words instead of 11. Same meaning. 6th grade.

### 2. One idea per sentence

If a sentence has two `that` / `which` / `because` clauses, break it.

❌ `Petrarch survived the Black Death, which had killed most of his friends, and decided that the problem with Italy was that the leaders cared more about their family honor than about the people.`
- One sentence, four clauses, 32 words.

✅ `Petrarch lived through the Black Death. Most of his friends did not. He looked at the wreckage of Italy and blamed the rulers. The lords cared more about their family honor than about the people, he wrote.`
- Four sentences, each one idea, all ≤15 words.

### 3. Concrete nouns over abstract ones

Pictures beat concepts. If the reader can see it, it lands.

| Abstract (cut) | Concrete (use) |
|---|---|
| lawlessness | bandits |
| the architectural achievement | the dome |
| classical erudition | a ten-year-old reciting Greek |
| consequence cascade | the next war |
| infrastructure | roads, walls, grain ships |
| leadership | the rulers, the lords |
| the state | Rome, Florence, France |
| socioeconomic conditions | thin soil, no food, bandits |
| centralized governance | one lord, his goons, his peasants |

**Worked transformation:**

❌ `The socioeconomic conditions of the post-Roman period gave rise to monarchical governance structures.`

✅ `Bad dirt grew villages, which grew lords, which grew kings.`

### 4. No jargon unless it's a named concept earning a bold

**Cut:** words that exist to sound smart. `Epistemology`, `bourgeoisie`, `teleology`, `dialectic`, `hegemony`, `codices`, `polity`.

**Keep:** words that are the **named concept** of the post — the term the reader will Google afterward. These earn one bold on first use:

- `**Eternal September**`
- `**political science**`
- `**Builder's Club**`
- `**philosopher princes**`
- `**reusable orbital heat shield**`

The bold tells the reader: this is the thing this post is about. Everything else uses plain English.

### 5. Active voice everywhere

Subject acts. Object is acted on. Verb sits between them, doing visible work.

❌ `The two who did were attacked by bandits on the way to visit him.`
- Passive. Bandits are the actors but they're hidden behind a prepositional phrase.

✅ `Bandits attacked them on the road.`
- 6 words instead of 14. Bandits land first. Reader sees the action.

❌ `A soft landing is not considered reusability.`
- Passive `is considered`.

✅ `A soft landing is not reusability.`
- Drop the hedge. State the fact.

## Audit checklist (run after first draft)

Run these greps mentally before delivering:

- [ ] Every prose sentence ≤15 words? (Quotes exempt.)
- [ ] Zero Latinate verbs from the cut list (table above)?
- [ ] Zero passive constructions? (`was -ed by`, `is being -ed`, `had been -ed`)
- [ ] Every abstract noun replaced with a concrete one or cut?
- [ ] One bolded named concept on first use — and nothing else bolded?
- [ ] No jargon left over from the source's academic register?

If three or more boxes fail, the post is reading at 8th grade or higher. Rewrite.

## What stays sophisticated

Hemingway clarity is **not** dumbing down. The post stays sophisticated through:

- The named concept (one per post, bolded)
- The specific historical / technical details from the source (40,000 tiles, September 1993, Cesare Borgia, Brutus's sons)
- The both-sides paradox in the body's reflective close
- The verbatim quotes from the speaker (which can use their natural register — Musk's `shucking tiles` stays)

The author voice is the part that gets simplified. The speaker, the facts, and the concept stay smart.

## Calibration anchor

When in doubt, ask: *"Could Hemingway have written this sentence?"*

If yes → ship.

If no → rewrite with a plainer verb, a concrete noun, or break it in two.
