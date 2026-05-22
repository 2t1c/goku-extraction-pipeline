# Topic Ranking — 6-criterion rubric for surfacing candidate ideas

When mining a transcript for candidate posts (SKILL.md Phase 1 step 2), score each candidate against these six proven viral patterns from past 1M+ impression posts. Surface the highest-scoring ideas first. Do not draft an idea below the Tier 3 threshold.

## The 6 criteria

Each criterion scored **0 / 1 / 2**:

- **0** — absent / does not apply
- **1** — present but weak
- **2** — strong / load-bearing for the post

### 1. Belief-confirming contrarianism

**Does it confirm what the target audience already suspects?**

Founders, investors, and curious operators (the @GeniusGTX audience) already suspect that institutions lie, that mainstream advice is mid, that the safe path is the expensive one, and that the people in charge are not as smart as advertised. A post that *names* one of these suspicions out loud — with a specific case study — converts.

- **2:** confirms a strongly-held suspicion in the audience's gut. *"AOL killed the early internet."* / *"Most VCs optimize the bets that won't matter."*
- **1:** confirms a mild hunch. *"Most platforms reward incumbents."*
- **0:** neutral observation or against-the-grain in a way the audience would resist.

### 2. Massive specificity

**Named expert + specific number, brand, body part, or institution.**

Generic claims slide past readers. Specific claims with names + numbers land. The hook formula already requires this (`[Speaker] says [named actor] [violent verb] [named target] [specific anchor]`) — this criterion measures whether the *content* below the hook has the same density.

- **2:** every body beat names something (Mosaic, $180M, September 1993, freshmen, Sulka shirts). The Andreessen "Eternal September" post is the canonical reference.
- **1:** some named anchors, but stretches of generic claim in between.
- **0:** abstract talk only — *"the trajectory was clear"*, *"the team grew"*, *"the market expanded"*.

### 3. Mechanism revealability

**Can the "why it works" be explained simply?**

A post that names *the mechanism* — the system, law, or process behind the surface fact — gives the reader something to teach someone else. That's what drives shares.

- **2:** post can teach the mechanism in 2–3 sentences without losing the reader. *"Eternal September: every fall, freshmen got college email, forums dropped in quality, then stabilized. AOL never let it stabilize."*
- **1:** there's a mechanism but it's hand-wavy / requires inside knowledge.
- **0:** no mechanism — just a surprising fact with no underlying *why*.

### 4. Buyable takeaway

**Protocol they can act on, OR argument they can deploy.**

The reader has to walk away with something usable — either a *thing they can do tomorrow* (protocol) or a *frame they can repeat at dinner* (argument). Posts that are "interesting" but not "buyable" cap out fast.

- **2:** clear takeaway. Protocol: *"Build the safety stack from week 3."* Argument: *"Capital papers over discipline until it doesn't."*
- **1:** implicit takeaway the reader has to derive on their own.
- **0:** no transferable lesson. Pure trivia.

### 5. Conspiracy / suppression layer

**Does the system look like the villain?**

When the post identifies a *structural* opposition — an institution, an industry norm, a category of expert that benefits from the truth staying hidden — engagement compounds. The reader feels they're being let in on something the gatekeepers don't want them to see.

- **2:** named institutional villain with clear incentive to suppress. *"Modern medicine isn't built to deliver miracle drugs cheaply."* / *"The body positivity movement was always a scam."*
- **1:** the system is implied as opposing but never named.
- **0:** no antagonist — the post is purely positive / discovery-flavored.

### 6. Everyday-behavior attack

**Does it target something they do without thinking?**

The strongest viral posts attack a *default behavior* the audience performs daily and never questions. Checking the calendar. Drinking the coffee. Going to medical school. Following the playbook. Posts that target a default behavior get screenshotted because the reader sees themselves in the trap.

- **2:** names a daily default the audience reflexively does. *"Naval deleted his calendar."* / *"Most founders apply for CEO jobs at companies they didn't start."*
- **1:** targets behavior that's common but not default-without-thinking.
- **0:** doesn't attack reader behavior at all — pure case study about somebody else.

## Scoring → tier mapping

Sum the scores (max 12). Map to tiers:

| Score | Tier | Estimated reach |
|---|---|---|
| **10–12** | **Tier 1** | 500K+ potential |
| **7–9**   | **Tier 2** | 100K–500K |
| **4–6**   | **Tier 3** | 50K–150K |
| **0–3**   | **Skip**   | Not worth drafting |

## Worked example — Baszucki interview, 5 candidate ideas

Each row shows the score per criterion, the total, and the tier.

| Candidate | (1) Contrarian | (2) Specific | (3) Mechanism | (4) Buyable | (5) Villain | (6) Behavior | Total | Tier |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **Roblox built on $10M; $500M-funded rival died** | 2 | 2 | 2 | 2 | 1 | 1 | **10** | T1 |
| **Tickets currency botted within a day** | 2 | 2 | 2 | 2 | 1 | 1 | **10** | T1 |
| **Eric Cassel built safety in week 3** | 1 | 2 | 1 | 2 | 0 | 1 | **7**  | T2 |
| **Roblox owns 40 data centers, < 1¢ / user / hour** | 1 | 2 | 1 | 1 | 0 | 0 | **5**  | T3 |
| **Bruno Mars set the music concurrency record** | 1 | 2 | 0 | 0 | 0 | 0 | **3**  | Skip |

Note: the Bruno Mars angle scores low because it's a one-time emergent event with no mechanism, no takeaway, and no villain. It's fun trivia, not viral substrate. Tickets scored a 10 because: contrarian (audience suspects "engagement gimmicks are gamed"), specific (Roblox, daily login, immediate botting), mechanism (any earnable currency gets farmed), buyable argument ("you can't pay users for time"), implied villain (the gimmick economy itself), targets default behavior (daily-login rewards everywhere in tech).

## Surfacing protocol (Phase 1 step 2)

When the user pastes a transcript:

1. Read top to bottom — **do not skim**.
2. List 8–15 candidate angles in your scratchpad.
3. Score each candidate against the 6 criteria.
4. Surface the top 5–10 in a table (rank, title, one-line rationale, total score, tier).
5. Drop anything scoring 0–3 — those won't earn the writing time.
6. Let the user pick from the surfaced set.

**Do not** surface a "balanced mix" across tiers. Surface the highest-scoring ideas, ranked. The user can ask for a Tier 3 angle if they want one for variety.

## What this rubric kills

- **Founder origin stories** that don't confirm a suspicion (criterion 1 = 0).
- **Quirky-history posts** with no mechanism the reader can teach (criterion 3 = 0).
- **Interesting-but-passive observations** with no buyable takeaway (criterion 4 = 0).
- **"Look how cool this company is" posts** with no antagonist (criterion 5 = 0).
- **Pure case studies** that don't reflect the reader's own behavior (criterion 6 = 0).

A candidate that scores 0 on three or more criteria is almost always not worth drafting, even if individual lines from the transcript are colorful. Move on.
