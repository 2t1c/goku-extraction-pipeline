# Hook Recipe — the actual formula

The repo previously said "specific shocking claim." That's too vague. Every shipped hook for @GeniusGTX follows a tighter recipe.

## The recipe

```
[Credentialed Name] says [named actor] [violent verb] [named target] [specific anchor].
```

Five slots. All five present. **Target 15 words. Hard cap 17.**

| Slot | What it is | Example |
|---|---|---|
| Credentialed Name | Title/role/company + name. Pick the **most powerful** phrasing under 6 words — not the shortest. See "The credential rule" below. | `Netscape founder Marc Andreessen`, `Renaissance historian Ada Palmer` |
| Verb | `says` or `reveals` — pick whichever fits the angle. `says` is the default; `reveals` when the claim is a hidden mechanism, suppressed fact, or insider knowledge. Never `claims`, `argues`, `believes`, `just revealed`, `recently said`. | `says` / `reveals` |
| Named actor | The protagonist of the claim — a person, company, or institution by name. Not "a founder", not "Big Pharma" generically. | `Elon`, `AOL`, `Michael Ovitz` |
| Violent verb | The dramatic action. See list below. This is the slot most people miss. | `killed`, `crushed`, `lit on fire` |
| Named target + anchor | What got hit, plus one concrete specific (number, date, visual detail). | `Hollywood with a 7am meeting and 20 identical Jaguars` |

## The credential rule

**Normally include the credential. Don't drop it just because the name is famous.**

- Format: `[Title / role / company] [Name]` — under 6 words.
- Pick the credential that does the most work for a cold reader scrolling X. Most powerful, not shortest.
- Credential types, in rough order of preference when multiple fit:
  - **Company association** when the company is more famous than the person — `Netscape founder`, `Roblox CEO`, `PayPal co-founder`, `a16z founder`
  - **Title + company** when both carry — `Tesla CEO`, `Nvidia CEO`, `OpenAI CEO`
  - **Profession** when the field anchors the claim — `Renaissance historian`, `Theoretical physicist`, `Longevity scientist`
  - **Institution** when prestige is load-bearing — `Harvard anthropologist`, `Yale professor`, `Stanford psychiatrist`
  - **Book/work** when the work is the speaker's main vehicle — `Inventing the Renaissance author`, `WEIRDest People author`
  - **Title alone** — `Dr.`, `Professor` — when nothing more specific helps
- **Bare name** (no credential prefix) is the exception, not the default. Only drop the prefix when the prefix would be redundant filler (`Tesla CEO Elon Musk` could be `Elon Musk` since he carries his own authority, but the prefix still does work).

### Don't lead with the dollar sign

The valuation/scale anchor belongs in the **claim**, not the credential prefix. Money/scale numbers earn their place by attaching to what's being said, not by tagging the speaker.

❌ `$1.4T Tesla CEO Elon Musk says Tesla can grab free power every night.`
✅ `Tesla CEO Elon Musk says Tesla can grab 500 gigawatts of free power every night.`

❌ `$50B Roblox CEO David Baszucki says Roblox runs as nine companies inside one.`
✅ `Roblox CEO David Baszucki says one company runs as nine inside a $50B shell.`

## Violent verbs — the live list

Use these. They carry the dramatic charge. Pick the one that's actually true to the source.

- `killed` — for systems, eras, industries that ended (`AOL killed the early internet`)
- `crushed` — for competitive demolition (`Ovitz crushed Hollywood`)
- `lit on fire` / `almost lit on fire` — for catastrophic risk (`Elon almost lit his $180M fortune on fire`)
- `broke` — for paradigms or institutions (`Musk broke aerospace`)
- `conquered` / `took over` — for market capture
- `buried` — for ideas or rivals deliberately suppressed
- `wiped out` — for industries or competitors annihilated
- `flipped` — for sudden reversal of conventional wisdom
- `swallowed` — for absorption stories (one entity consumed by another)
- `gutted` — for hollowing out from within
- `outsmarted` — for clever underdog wins
- `humiliated` — for public defeats
- `predicted` (only if dramatic prediction came true) — `predicted X years before it happened`
- `warned` (only if catastrophe followed and was ignored)

**Bland verbs to avoid in hooks:** `built`, `created`, `started`, `said`, `did`, `made`, `worked on`, `helped`. They describe; they don't dramatize.

## The anchor — pick one, not three

Every hook has exactly one specific concrete:

- **Number**: `$180 million`, `two million users`, `20 Jaguars`, `7am meeting`
- **Date**: `September 1993`, `in 1975`, `on a single day`
- **Visual detail**: `identical Armani suits`, `wreckage of the third rocket`
- **Named entity in object position**: `Mosaic`, `the Greek agora`

If a hook has zero anchors it sounds vague. If it has three it sounds like a list. Pick the sharpest one and front-load it.

## "One X" framing — when one beats many

When you can choose between `one [thing]` and a specific count like `40,000 [things]`, **prefer "one"** for the hook. Counterintuitive, but it's a curiosity lever:

- A large number tells the reader the size of the problem upfront. They know how big it is. They have an answer.
- `One X` forces the reader to ask *which one?* It opens a loop the body has to close.

**Examples (experimental-hemingway branch):**

✅ `Elon Musk says one heat shield problem could kill Starship's reusability for years.`
- Reader thinks: *which one problem?* They click to find out.

❌ `Elon Musk says 40,000 tiles could kill Starship's reusability for years.`
- Reader already has the size of the problem. Less mystery. The 40,000 anchor belongs in the body, where it pays off the open loop.

---

✅ `Ada Palmer says one Renaissance city was so notorious that visiting it once was court evidence in France.`
- *Which city? What evidence?* Loop opens.

❌ `Ada Palmer says Florence so dominated sodomy that France used it as court evidence.`
- All the named entities are spent in the hook. Loop pre-closes.

---

**When to use the count anyway:**

- The count IS the shock and there's no path to "one" framing — `Musk says SpaceX will launch 10,000 Starships a year — one every hour.` (Here the count IS the claim; trying to obscure it makes the hook weaker.)
- The count is a paradox-anchor, not a quantity-anchor — `Andreessen says AOL killed the early internet on a single day in September 1993.` ("A single day" works *because* it's small, not despite being a count.)

**Rule of thumb:** if the body's job is to reveal a specific concrete answer, hide that answer in the hook. Lead with `one` and let the body deliver the number, the name, or the visual.

## Worked transformations

**Bland → Goku:**

❌ `Marc Andreessen reveals how Elon spent his fortune on rockets.`
- No violent verb (`reveals` is journalist-passive). No anchor. Conventional verb (`spent`).

✅ `Marc Andreessen says Elon almost lit his entire $180 million fortune on fire making rockets.`
- Violent verb (`lit on fire`), named actor (`Elon`), specific anchor ($180M), action context.

---

❌ `Marc Andreessen explains how AOL changed the early internet in 1993.`
- `explains` and `changed` are both bland. Reads like a Wikipedia subhead.

✅ `Marc Andreessen says AOL killed the early internet on a single day in September 1993.`
- `killed` carries the drama. `on a single day` makes the date hit harder than `in 1993`.

---

❌ `Marc Andreessen recalls how Michael Ovitz built CAA into a powerhouse.`
- Wistful verb (`recalls`), bland verb (`built`), abstract noun (`powerhouse`).

✅ `Marc Andreessen says Michael Ovitz crushed Hollywood with a 7am meeting and 20 identical Jaguars.`
- `crushed` is the violent verb. The anchor (`7am meeting + 20 Jaguars`) is visual and specific.

## What to do when the source doesn't fit the recipe

Sometimes the source is a thoughtful observation, not a clash. Two options:

1. **Find the violence inside it.** Most "interesting observations" contain a hidden adversarial frame. "Ovitz worked harder" → "Ovitz crushed agencies that started at 9am." Look for what got destroyed, displaced, or rendered obsolete.

2. **Skip the angle.** If it genuinely doesn't fit a clash structure, it's probably a Tier 3 idea. Don't force it into the hook recipe — pick a different idea from the candidate list.

Do **not** ship a hook without a violent verb. The whole feed reads as polite if every post starts with `says X built` or `says X explained`.

## Word count — recommended 15, hard cap 17

| Word count | What to do |
|---|---|
| 11–14 | Sweet spot. Ship. |
| 15 | Target. Ship. |
| 16–17 | Allowed when the extra word(s) preserve credential strength or a specific anchor. Don't trim out of habit. |
| 18+ | Trim. Drop articles, adverbs, full names → last names. **Trim the claim, not the credential.** |

Worked examples:

- 13 words: `Marc Andreessen says AOL killed the early internet in September 1993.`
- 14 words: `Renaissance historian Ada Palmer says Petrarch's plan to revive Roman virtue produced Cesare Borgia.`
- 15 words: `Marc Andreessen says Elon almost lit his entire $180 million fortune on fire making rockets.`
- 16 words: `Nvidia CEO Jensen Huang says one chip generation will leap from one million to ten million units.`
- 17 words: `Netscape founder Marc Andreessen says AOL killed the early internet on a single day in September 1993.`

If you're at 18+, drop a word. Usually it's an article (`the`), an adverb (`almost`, `nearly`), or a full first name where the last name carries (`Ovitz` not `Michael Ovitz`). **Never trim the credential to fit; trim the claim.**
