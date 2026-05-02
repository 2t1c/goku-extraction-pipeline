# Post Quality Checklist

Run this before delivering any draft. **Every box must check.** If any fails, rewrite before showing the user.

## Hook (15 words max)

- [ ] Format: `[Credentialed Name] says [specific shocking claim]`
- [ ] Verb is exactly `says`. Not `just revealed`. Not `recently said`. Not `now believes`.
- [ ] No recency words anywhere: no `just`, `now`, `today`, `this week`, `breaking`, `recently`
- [ ] Credential is the shortest phrase that establishes authority (e.g. `Sequoia's`, `Netscape founder`, `Dr.`)
- [ ] Claim is one specific shocking thing — named person, specific number, or paradigm-break

## Body (240–250 words)

- [ ] **Counted, not estimated.** Actual word count is in the 240–250 range.
- [ ] Every prose sentence ≤15 words. Quotes exempt. At most one sentence over 15.
- [ ] 2–4 direct verbatim quotes from the transcript.
- [ ] Reported speech only. No first-person voice in body. No "I think", no "in my view".
- [ ] No tabloid adjectives: no `shocking`, `unbelievable`, `jaw-dropping`, `insane`, `crazy`, `mind-blowing`.
- [ ] No recency words anywhere in the body.
- [ ] If bullets are used: 3+ parallel items, 3–6 words each, sentence fragments.
- [ ] Body lands on a sharp line — ideally a verbatim quote.

## Closer (after body, in this order)

- [ ] **Engagement Q**: simple binary opinion question, ≤8 words ideally. Not "where in your life is...".
- [ ] **Brand CTA**: VERBATIM as in `closer-template.md`. Not paraphrased.
- [ ] **P.S. Product CTA**: VERBATIM as in `closer-template.md`. Includes the Gumroad URL inline.
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

- [ ] Notion sub-item title matches the post hook claim (or a short distillation)
- [ ] Topic Tags set (1–4 from the schema)
- [ ] Parent video relation linked
- [ ] Local clip path in body for manual fallback: `~/Desktop/AI Agents/clips/<slug>.mp4`

## If the user has standing rules from past sessions

Always check `~/.claude/projects/.../memory/feedback_*` for the latest preferences. If a rule there contradicts this checklist, the memory rule wins (it's the more recent decision).

Currently active feedback rules (May 2026):

- Engagement Q must be simple binary
- No recency words in posts
- Word count target 240–250
- Spaced handles in attribution
- Manual drag-drop or parallel API attach for Typefully (user-controlled)
- Slug naming for clip files
- Pre-cut clip in parallel with draft delivery
- Clip output to `~/Desktop/AI Agents/clips/`

If any of these conflict with what this checklist says, do what the memory rule says — it's the more recent decision.
