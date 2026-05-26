# Closer Template — student edition (May 2026)

The closer is the last elements of every long-form Goku post. **Product + Brand CTA wording is verbatim per batch. The body one-liner and attribution are written fresh per post.**

> **Student note:** This file uses `{{BRAND_HANDLE}}`, `{{BRAND_DESCRIPTION}}`, `{{PRODUCT_NAME}}`, `{{PRODUCT_DESCRIPTION}}`, `{{PRODUCT_SOCIAL_PROOF}}`, `{{PRODUCT_URL}}`, and `{{DM_KEYWORD}}` placeholders. Fill them in once for your account (see `STUDENT_SETUP.md`). The filled-in example at the bottom shows what one looks like for GeniusGTX.

## Order

After the body ends, in this exact order:

1. **Body One-Liner Close** (the last line of the body itself — a reflective punch that lands the post's central tension)
2. **Product CTA** (verbatim — the paid playbook, comment-to-DM mechanic)
3. **Brand CTA** (verbatim)
4. **Attribution** (write fresh, with spaced @handles)

> **Note:** The engagement question that used to sit at position 1 is **deprecated on this branch**. See "What's removed" below for context. Every post on this branch ends the body itself on a reflective one-liner — no question prompt follows it.

### 1. Body One-Liner Close (write fresh, story-rooted, reflective)

**The last line of the body is the closer.** It's the reflective punch the post has been building toward — usually one line, sometimes two, sitting on its own line with white space around it. The reader closes the story themselves; we don't prompt them with a question.

**The shape that works:**
- Pays off the central tension of the story you just told
- Reads as a sentence, not a question
- Lands on a concrete image, a both-sides paradox, or a stake-naming statement
- One sentence, ≤15 words (per the body sentence cap)
- Sits on its own line with white space above and below

**Good examples (from posts on this branch):**

| Post topic | One-liner close |
|---|---|
| Italy topsoil → republics | *"Someone was feeding Florence."* |
| Cosimo's Greek cosplay | *"They were the **weapon**."* |
| Petrarch's plan → Borgia | *"That was the war Machiavelli watched."* |
| Machiavelli's pivot | *"That is the road to science."* |
| Florence as a verb | *"…the connection was not a coincidence."* |
| Leonardo as saboteur | *"A **saboteur** of progress is what Leonardo had been the whole time."* |
| Musk's heat shield | *"The reusable heat shield is the last gate to Mars."* |

**Why a reflective one-liner beats an engagement Q:**

- The post already walked the reader through a specific tension. The one-liner lands that tension as a statement they can carry, not a question they're being quizzed on.
- The engagement Q template made every post end on the same beat — quiz prompt → CTA. The one-liner lets each post end on its own native sign-off.
- The algorithm increasingly rewards thoughtful comments over one-word reactions to A/B prompts. Statement closes that name a paradox or a stake invite **real** replies — readers volunteer their own framing.
- Reads as essay, not BuzzFeed.

**Avoid:**
- Engagement questions of any form (deprecated on this branch — see below)
- Author voiceover ("This is why X matters", "And that's the lesson") — laid on top of the story
- Soft summaries ("So the next time...", "In the end...")
- Setup-without-payoff closers that read as cliffhangers

### 2. Product CTA — fixed verbatim, drop-in (comes BEFORE Brand CTA)

The Product CTA is the same on every post. **Don't personalize. Don't theme-tie. Don't agitate.** The body already did the narrative work; the Product CTA is just the clean handoff to the product. Same wording every time, with blank lines between paragraphs for breathing room.

Two mechanics are valid. Pick **one** per batch — never mix on the same post.

---

#### Option A — Direct URL (use for free products)

```
P.S. I made {{PRODUCT_DESCRIPTION}}.

{{PRODUCT_SOCIAL_PROOF}}

{{CTA_LINE}}

{{PRODUCT_URL}}
```

**Order matters:** offer line (the product) → social proof (optional, real numbers only) → CTA line → URL.

**Drop the `{{PRODUCT_SOCIAL_PROOF}}` line entirely if you don't have real numbers** — made-up proof corrodes trust.

**Filled-in GeniusGTX example (production wording):**

```
P.S. I made a playbook breaking down 100+ most powerful decision making mental models used by history's greatest thinkers.

5,000+ downloads. 113 five-star reviews.

Grab a free copy here:

https://besuperhuman.gumroad.com/l/mentalmodels
```

---

#### Option B — Comment-to-DM (use for paid products)

```
P.S. {{STORY_ROOTED_BRIDGE}}

As {{AUTHORITY}} said: "{{AUTHORITY_QUOTE}}"

So I {{PRODUCT_ORIGIN_LINE}}.

Comment "{{DM_KEYWORD}}" and I'll send you the details.
```

**Four-beat structure:** story-rooted bridge → third-party authority quote on the frame → product line → comment-to-DM call.

**No URL in the P.S.** The comment is the gate. When the reader comments `{{DM_KEYWORD}}`, you (or your automation) DM them the paid link — the gating qualifies intent so you can send the right context.

**Filled-in GeniusGTX example (Incentives book):**

```
P.S. Pull the thread on any story like this and you'll find the hidden incentive at the other end.

As Munger said: "Show me the incentive and I'll show you the outcome."

So I wrote a short book on how to spot them and design your own.

Comment "INCENTIVES" and I'll send you the details.
```

---

**Why two mechanics, not one:** free product → direct URL (lowest friction; we want everyone to grab it). Paid product → comment-to-DM (qualify intent, control the link). Don't cross the wires.

### 3. Brand CTA (verbatim — never change, comes AFTER Product CTA)

```
If you're new here, follow {{BRAND_HANDLE}} for content on {{BRAND_DESCRIPTION}}.
```

**Filled-in GeniusGTX example:**

```
If you're new here, follow @GeniusGTX for content on the greatest minds in economics, psychology, and history.
```

**Why fixed beats personalized:**
- The body already did the personal/narrative/insight work. The reader gets the personal connection from the *post*, not the P.S.
- Personalized P.S. paras drift toward "second body" length and feel salesy. Fixed wording is a clean signal: "post over, here's the offer, take it or scroll."
- Consistency across posts is a feature — readers who see your closer once recognize it the next time and click without thinking.

**Line spacing rule (still applies):** blank lines between every short paragraph. The last 4 lines of the post are what the reader sees right before deciding to click; cramming them into one block reads as overwhelming. Each line breathes.

### 4. Attribution (write fresh, with spaced @handles)

Format:

```
— [Expert Name] ( @handle ), [credential], on [Host Name]'s ( @host_handle ) [Show Name]
```

**Critical:** add single spaces inside parentheses around every @handle. Without spaces, X's auto-mention engine doesn't render the tags as clickable links.

✅ `— David Baszucki ( @DavidBaszucki ), founder & CEO of Roblox, on David Senra's ( @davidsenra ) Founders podcast`

❌ `— David Baszucki (@DavidBaszucki), founder & CEO of Roblox, on David Senra's (@davidsenra) Founders podcast`

## What's removed from the old format

- The old "bridge / reciprocity lens" intro ("One pattern worth keeping...", "One lens worth keeping...") is **deprecated**.
- The comment-to-DM mechanic (*"Comment 'models' and follow @GeniusGTX so I can DM you a copy."*) is **deprecated** — current P.S. ships a direct Gumroad URL (`https://besuperhuman.gumroad.com/l/mentalmodels`). No operator middle step.
- The pain/desire one-liner (*"So if you want to stop overthinking, control chaos, and navigate any decision with the clarity..."*) is **deprecated** — replaced by the social-proof line (*"5,000+ downloads. 113 five-star reviews."*) + a direct *"Grab a free copy here:"* CTA line.
- The "full playbook breaking down the timeless decision-making mental models" wording is **deprecated** — current phrasing is *"a playbook breaking down 100+ most powerful decision making mental models"* (concrete count over the vague "timeless").
- The Feynman/Munger/Musk strategist credential line and the "Trusted by 5,000+ founders and investors" social proof line are both **deprecated** — current P.S. is offer line + downloads/reviews proof + URL.
- The earlier PAS-personalized P.S. para 1 (with theme-tied agitation) is **deprecated** — the P.S. is now drop-in fixed wording on every post.
- The earlier Brand CTA wording (*"@GeniusGTX is a gallery for the greatest minds in economics, psychology, and history. Follow along for more similar content."*) is **deprecated**. Current Brand CTA is the shorter version: *"If you're new here, follow @GeniusGTX for content on the greatest minds in economics, psychology, and history."*
- Formulaic A/B binary engagement questions (`"Genius — or ruthless?"`, `"Capital or discipline?"`) are **deprecated**.
- **All engagement questions of any form are deprecated on the `experimental-hemingway` branch.** The body itself ends on a reflective one-liner. No question prompt follows the body. Rationale: every post ending on the same quiz-prompt beat made the feed feel templated. Statement closes feel like essays. See "1. Body One-Liner Close" above.

## Full example (Petrarch post, on this branch)

```
That was the war Machiavelli watched.

P.S. I made a playbook breaking down 100+ most powerful decision making mental models used by history's greatest thinkers.

5,000+ downloads. 113 five-star reviews.

Grab a free copy here:

https://besuperhuman.gumroad.com/l/mentalmodels

If you're new here, follow @GeniusGTX for content on the greatest minds in economics, psychology, and history.

— Ada Palmer ( @Ada_Palmer ), Renaissance historian at the University of Chicago, on Dwarkesh Patel's ( @dwarkesh_sp ) podcast
```
