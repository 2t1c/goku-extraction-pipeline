# Clip Selection — Standalone Hook Rule

The video clip that pairs with each post is **content in its own right**, not a footnote to the X post. Someone scrolling past who watches *only* the clip should be hooked in 2–3 seconds.

## The hard rule

The clip's **first sentence** must function as a standalone hook. It must do at least one of:

1. **Drop a named authority with a shocking claim.** "[Expert Name] says [X]." If the expert is the speaker, their first audible line must be the claim itself.
2. **Open on a dramatic reversal or pattern interrupt.** "Bodybuilders die decades earlier." "Managers are failing at every industry that's changing."
3. **Open on a cryptic arresting statement** that creates a curiosity gap. *"Yes. Zero. As little as possible."* works because the cold viewer wonders *zero what?*
4. **Open on a specific number, named person, or concrete fact.** "DARPA gave the search algorithm to two Stanford students." "Starlink just hit 10 million subscribers."

## Banned start cues

- **Transitional / meta lines.** "So there's this thing where...", "The book I always recommend...", "Let me tell you a story...", "So this is interesting..."
- **Dangling pronouns.** "And he said that...", "This is what's happening now..." — cold viewer has no referent.
- **Host questions or setup.** Cut past to the expert's answer.
- **Soft hedges.** "I think maybe...", "It's sort of like...", "You could argue that..."

## Selection protocol

When picking a clip for an approved post, run these in order:

1. **List the post's load-bearing beats** — every claim, named person, number, and direct quote in the post body.
2. **Locate each beat in the transcript.**
3. **Find the tightest window that covers the most beats.**
4. **Scan the first 30 seconds of the candidate window for a sentence that passes the standalone hook test.** The clip starts on the *hookiest* sentence, not the narratively-first one.
5. **Pick an end cue that lands with finality.** A sharp claim, a punchline, a quote, a stark statement. Not a trail-off.
6. **Verify quote coverage.** Every quoted phrase in the post must appear in the clip. If the hookiest opener sits outside the window needed to cover quotes, expand the window or change the post.

## Length

- **Sweet spot:** 2:30–3:30
- **Hard floor:** 1:00 — never under, even when the source feels dense. The clip needs enough breathing room for the speaker to actually deliver an insight, not just a one-liner. If the cue range comes back under 1:00, **extend the end cue** to capture the next coherent beat the speaker delivers, or **back the start cue up** to include more setup (as long as the start line itself isn't a banned transitional/hedge).
- **Hard ceiling:** 4:00 (algorithm dilutes attention beyond)

## Captions

Burned-in captions are optional. Hand-timed captions don't work — they drift. If captions are wanted, install `mlx-whisper` (Apple Silicon) or `whisper-cpp` for word-level timing, then use `scripts/burn_captions.py`.

## Examples from the wild

### Pass ✅

- *"Yes. Zero. As little as possible."* — Andreessen on introspection. Cryptic + arresting + curiosity gap.
- *"Elon's not the first guy who said, 'We're going to do satellite-based internet access.'"* — Andreessen on Starlink. Names Elon + pattern interrupt + curiosity (who came first?).
- *"I don't take vacations."* — Elon (quoted by Andreessen). Direct, cold, arresting.
- *"It basically turns out every new technology is greeted with what they call a 'moral panic.'"* — Andreessen on bicycle-face. Named concept + universal claim.

### Fail ❌

- *"The book that I always recommend on this topic is called 'The Machiavellians.'"* — Andreessen on managerialism. Reads as setup; cold viewer hears "here's a book I like" and scrolls.
- *"And he said that..."* — dangling pronoun, no antecedent for cold viewer.
- *"So basically, what happens is..."* — meta filler.
