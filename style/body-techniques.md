# Body Techniques — what makes a Goku body land

Beyond the rules in `master-prompt.md` and `word-count.md`, the actual shipped posts use a small set of recurring **techniques**. Each one is earned by the source — don't force them. But a strong post usually deploys 2–3 of these.

## 1. The number cascade

Compress time/scale by listing escalating numbers in a single beat.

> "The smartest two million were swallowed by the next two million, then twenty million, then five billion."

Single sentence (quotes-exempt from the 15-word cap). Four numbers, no commentary. Reader does the math. Use when the source supports a growth/scale arc — internet users, cap raises, audience size, casualties, prison populations.

## 2. The verbatim dialogue exchange

Place 2–4 short quotes back-to-back as a theatrical exchange. Each line on its own paragraph.

> Your agent: "They don't represent you."
>
> You: "Yeah, isn't it great?"

This is the technique that makes the Ovitz post land. Use when:
- The speaker reconstructs a conversation in the transcript
- Two parties are speaking past each other
- The punchline is in the second voice

Don't fabricate dialogue. If the speaker imagines what someone said, mirror that hedge: `Andreessen's reconstruction of the call:` then the dialogue.

## 3. The closing paradox

End the body with a two-beat reversal. Same noun, opposite verbs.

> "He was wrong about the rockets. But he was right about the fire."

Variations:
- `Wrong about X. Right about Y.`
- `Saved Z. Lost W.`
- `Got the question right. Got the answer wrong.`

Earned when the source contains a tension that pays off. Don't manufacture paradox — readers can smell it.

## 4. Speaker stake in prose

Establish the speaker's relationship to the event **inside the body**, not in a credentials paragraph.

> "Andreessen, who was building Mosaic at the time, watched it happen."

This carries 3× the weight of `Andreessen, co-founder of a16z and former Netscape engineer, comments…`. Find the one specific thing the speaker was doing **at the moment of the story**. That's their stake. Use it once, mid-body.

## 5. The before / then structure

Two paragraphs. First establishes the world. Second pivots.

> Before that day, the internet had maybe two million users.
>
> They were the smartest two million people in the world.
>
> Andreessen says it felt like Athens in 500 BC.
>
> [...]
>
> Then America Online bought a connection to it.

The pivot word is `Then`. Or `Until`. Or `One day`. Single-syllable, no adverb decoration. The reader feels the hinge.

## 6. The named-concept boldface

If the source contains a shareable handle (`Eternal September`, `Kleiber's Law`, `the Lindy Effect`, `managerialism`), bold it on first use.

> It became known as **Eternal September**.

This is the term someone Googles after the post. Bold so it doesn't dissolve into the body. **One bold per post**, max — more than one and the technique loses force.

## 7. The visual detail trio

Three concrete sensory specifics, often in a fragment list.

> Twenty agents would arrive at every premiere. Identical Armani suits. White shirts from Sulka in Beverly Hills.
>
> Twenty Jaguars in the parking lot, plates running CAA-1 through CAA-20.

Brand names (Armani, Sulka, Jaguar). Specific counts (twenty, twenty). Specific identifiers (CAA-1 through CAA-20). The reader sees it.

Use when the speaker provides cinematic detail. Don't invent details to fill the slot — readers can tell.

## 8. End the body on a verbatim quote OR a reflective one-liner

Highest-leverage move. Let the speaker have the last word — or land a reflective one-liner that pays off the central tension.

(On the `experimental-hemingway` branch, there is no engagement question following the body. The body's last line **is** the close. See `closer-template.md`.)

> Andreessen, looking back:
>
> "I'm pro that. I'm glad that happened. But the pro and the con of that is that took the internet from this ivory tower kind of thing to this basically mainstream consumer ordinary people thing."

The lead-in (`Andreessen, looking back:`) is a single short fragment. The quote does the work.

Alternatives that also land:
- A paradox (technique 3)
- A single-sentence stark statement: `The September never ended.`

Avoid ending on your own paraphrase. The reader's last impression should be the speaker's voice or a sharp authored line — never a soft summary.

## 9. The hedge preservation

If the speaker hedges in the source (`I think it was Adeo Ressi, or someone…`), the post hedges too:

> The friend (Andreessen thinks it was Adeo Ressi) sat Elon down before he started SpaceX.

Don't confidently attribute what the speaker hedged. The hedge is part of the truth — and stripping it makes the post fragile to fact-checks.

## 10. Setup-before-long-quote

**Rule:** any verbatim quote longer than ~15 words gets a plain-English setup sentence in front of it. The setup tells the reader what the quote is going to do, in 4th-grade vocabulary. Then the quote can use its full register — Musk's `shucking tiles`, Andreessen's `ivory tower`, Palmer's `philosopher princes` — without losing the reader.

**Before (drops the reader cold):**

> "It's gotta make it through the ascent phase without shucking a bunch of tiles, and then it's gotta come back in and also not lose a bunch of tiles or overheat the main airframe."

The reader has to parse `shucking tiles` and `ascent phase` without any anchor. By the time they figure it out, they've stopped reading.

**After (setup carries the reader in):**

> The shield has two jobs and they fight each other.
>
> Going up, it has to survive the ascent without losing tiles. Coming back down, it has to hold the airframe together through reentry without burning through.
>
> *"It's gotta make it through the ascent phase without shucking a bunch of tiles, and then it's gotta come back in and also not lose a bunch of tiles or overheat the main airframe."*

The reader now has the concept in plain English before they hit the technical quote. The quote becomes texture and authority — Musk's actual voice on the problem — instead of a wall the reader has to climb.

**When the setup is required:**
- Quote contains jargon (`shucking`, `airframe`, `consensus mechanism`, `quorum`)
- Quote contains a proper noun the audience doesn't know cold (`Brutus`, `Marsilio Ficino`, `the Officers of the Night`)
- Quote is longer than ~20 words
- Quote uses sentence structure that takes a second pass to parse

**When you can skip the setup:**
- Quote is short (≤15 words) and self-contained
- Quote is the **payoff** of a setup the prose already did
- Quote IS the named concept (`"It became known as the Eternal September."`)

The setup is what keeps the body at 6–7th grade reading level even when the speaker's quotes naturally sit at 10–12th. See `hemingway-clarity.md`.

## Combining techniques — the gold-standard pattern

The Ovitz post (gold standard) uses:
- Speaker stake in prose (technique 4): "Ovitz did one thing differently."
- Before / then (technique 5): the 9am-vs-7am pivot
- Verbatim dialogue exchange (technique 2): the Paul Newman call
- Visual detail trio (technique 7): Armani, Sulka, Jaguar
- Named-concept boldface (technique 6): not used here, no shareable term

Most strong posts deploy 3–4 techniques. Fewer than 2 and the body feels like a summary. More than 5 and it feels overstuffed.

## What NOT to do

- **Don't open the body with a credentials paragraph.** "Andreessen is a co-founder of Andreessen Horowitz, formerly the engineer behind Netscape, and a venture capitalist…" — kill it. Use technique 4 (speaker stake in prose) instead.
- **Don't summarize the speaker.** "Andreessen has spent decades thinking about…" — soft, abstract, kills momentum. Replace with a quote or a specific scene.
- **Don't add your own thesis.** "What this really shows is…" — there's no `you` in a Goku post. Reported speech only.
- **Don't end on a question that isn't the engagement Q.** The body ends on a quote or sharp line. The engagement Q is a separate beat *after* the body.
