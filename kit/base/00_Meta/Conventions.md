---
type: meta
title: Conventions — Metadata, Tags & Linking Spec
summary: "The source-of-truth spec for the vault: frontmatter fields (including the required summary), note atomicity and split heuristics, the tag taxonomy, linking rules, capture, and tiered retrieval."
aliases: [Conventions, Schema, Metadata Spec]
created: 2026-07-27
updated: 2026-07-27
tags: [meta/conventions]
related: ["[[AGENTS]]"]
---

# Conventions

The **source of truth** for how notes are structured. [[AGENTS]] is the quick guide; this is the detailed spec. Keep them consistent.

## Frontmatter fields

| Field | Required | Applies to | Notes |
|---|---|---|---|
| `type` | ✅ always | all | One of: `meta`, `moc`, `profile`, `experiment`, `project`, `person`, `topic`, `source`, `daily`, `org`, `idea`, `analysis`, `decision`. Drives all queries. |
| `title` | ✅ | all | Human-readable title (filename can differ). |
| `summary` | ✅ always | all | **One or two sentences, plain text, no wikilinks.** The machine-readable preview an agent reads *before* opening the note. This is the single most important field for fast retrieval — it is what shows up in [[INDEX]] and lets an agent decide relevance without loading the whole note. Write it so it stands alone. |
| `aliases` | recommended | all | Alternate names/synonyms so links/search resolve. Add real synonyms an agent might grep. |
| `status` | ✅ for experiment/project/idea | experiment, project, idea | `idea` · `active` · `paused` · `done` · `abandoned`. |
| `created` | ✅ | all | `YYYY-MM-DD`. |
| `updated` | ✅ | all | `YYYY-MM-DD`. Refresh on every edit. |
| `tags` | recommended | all | Hierarchical, see below. |
| `related` | optional | all | List of wikilinks, e.g. `["[[Note A]]", "[[Note B]]"]`. |
| `provenance` | optional | all | How the note's core claims were obtained: `stated` (you said it) · `verified` (checked against a repo/paper/data) · `inferred` (agent inference, mark inline too) · `mixed`. Lets an agent weigh a hard fact vs a synthesis. |
| `confidence` | optional | analysis, inferred facts | `high` · `medium` · `low`. Use when a claim is uncertain. |

Type-specific optional fields:

- **experiment**: `hypothesis`, `started`, `ended`, `result` (`success`/`partial`/`failure`/`inconclusive`).
- **project**: `started`, `target`, `stack` (list), `repo`, `url`.
- **person**: `relationship`, `met`, `birthday`, `location`.
- **source**: `author`, `url`, `kind` (`article`/`book`/`paper`/`video`/`podcast`), `rating`.
- **org**: `website`, `industry`, `location`. One note per organization (employer, company, lab), stored in `Orgs/`; link people to it.
- **daily**: just `type: daily`, `summary`, `created`, `tags`.
- **idea**: a raw, unrefined spark captured in `Ideas/`. `status: idea` by default; promote to a `project` or `experiment` when it matures (then link back).
- **topic**: an **atomic concept note** — one idea, one model, one loss, one mechanism (the reusable knowledge unit). Lives in `Knowledge/`. See "Note size & atomicity" below — this is the type you want *many* of.
- **analysis**: an **agent-generated synthesis filed back from a conversation** — a comparison, multi-note analysis, decision rationale, or plan that's worth keeping rather than losing to chat. Lives in `Analyses/`. Optional fields: `source` (e.g. `conversation (2026-06-25)`), `question` (the prompt that generated it). Mark it clearly as agent-derived (not an external source). See the "file answers back" rule in [[AGENTS]] §4.
- **decision**: a **commitment the user made, and why** — binding on future work until explicitly reversed. Lives in `Decisions/`. One decision per note; the `summary` states the decision itself so an agent can honor it without opening the note. If a later decision overrides it, link the two and say so.

## Note size & atomicity (read this)

**A note is a retrieval unit.** Whether an agent uses embeddings/RAG or plain `grep`, note size determines retrieval quality: one small note about one idea produces a sharp match and loads little context; one big note about ten ideas produces a fuzzy match and forces the agent to wade through nine irrelevant sections. **Prefer many small, self-contained, densely-linked notes over few large ones.**

**Target:** one concept per note, roughly **100–400 words** for a `topic`/atomic note. There is no hard word limit — atomicity is about *conceptual completeness*, not length. Use these tests:

- **Naming test** — if you can give it one specific title, it's probably atomic. If the title needs "and"/"&"/a list, it's probably two notes.
- **Glance test** — understandable at a glance.
- **Necessity test** — nothing missing for it to stand alone when retrieved in isolation.

**Self-contained but linked.** Each note must make sense on its own (it may be retrieved without its neighbours), *and* link outward with `[[wikilinks]]` to related notes and its hub. Put enough context in the note to stand alone; link for the rest.

**Hubs are allowed to be big.** `project`, `moc`, `analysis`, `daily`, and running logs are *hubs/records*, not atomic units — they may be long. But a project note should **delegate reusable detail to child `topic` notes and link them**, keeping itself a navigable overview (status, decisions, links) rather than a dumping ground.

**When to SPLIT a note into atomic notes:**
- It contains more than one reusable building block (e.g. a concept + an argument + a result).
- A section has its own natural title — that heading is usually a latent atomic note.
- You find yourself wanting to link to *part* of the note — that part should be its own note.
- An agent would have to load a lot of irrelevant text to answer a narrow question about it.

**Keep together when** splitting would break a tightly-coupled unit, or the pieces fail the necessity test on their own, or it's an early-stage hub where context matters more than purity. Atomicity is a compass, not dogma — usability for the next agent (and future-you) is the goal.

**Decomposition procedure (additive, non-destructive — the default):** (1) list the note's headings/claims; (2) each distinct reusable building block becomes a new `topic` note in `Knowledge/` with its own `summary` + tags; (3) link the new note back to the source note and to related notes; (4) in the source note, link out to the new child note (leave the original text in place unless you've OK'd slimming it). This grows the graph without losing anything.

## Capture: log anything, process later

The point of a second brain is to **capture with zero friction, then let agents do the processing.** Two capture zones:

- **[[Inbox]]** (`Inbox.md` at the vault root) — a single always-there dumping ground. Drop any half-formed thought, link, or fact as a bullet, any time, no frontmatter, no filing decision. Ask your agent to process it (`/second-brain capture` writes to it; any agent session can be asked to sort it) — durable items get promoted into proper atomic notes (linked), ephemeral ones discarded.
- **Daily notes** (`Daily/YYYY-MM-DD.md`) — dated fleeting capture tied to a day. Durable items get promoted into notes and linked.

Nothing is "too small to log." A one-line fact, a preference, a gotcha, a name — capture it; the agent atomizes and links it later.

## Tiered retrieval (how an agent should read the vault)

Read cheap-to-expensive, stop as soon as you have enough:
1. **[[INDEX]]** — flat catalog of every note by `type`, each with its `summary`. Scan this first.
2. **`summary` frontmatter** of the candidate notes — decide relevance without opening bodies.
3. **Full note** — open only the ones that matter.
4. **Raw sources** — repos/papers/data linked from the note, last.

This is why `summary` is required and why notes should be atomic: it keeps the agent's context small and its search precise.

## Tag taxonomy

Use **hierarchical** tags (`parent/child`) so they group cleanly. Lowercase, no spaces (use `-`).

Structural tags (what kind of note):
`#meta` · `#moc` · `#experiment` · `#project` · `#person` · `#topic` · `#source` · `#daily`

Domain tags (what it's about) — start a small vocabulary that fits your life/work and reuse it; a starting point:
`#ai` · `#health` · `#fitness` · `#finance` · `#career` · `#learning` · `#writing` · `#productivity` · `#relationships` · `#travel` · `#hobby`

State tags (optional, for quick filtering):
`#todo` · `#waiting` · `#idea` · `#reference`

> [!note] Before inventing a new tag, grep existing tags to avoid near-duplicates (`#health` vs `#wellness`). Keep the vocabulary small — 5 consistent tags beat 20 inconsistent ones.

## Tasks (optional convention)

If you want real to-dos to stand out from scaffolding checklists, mark actionable ones with a distinct trailing marker (e.g. `#task` or, if you use Obsidian's Tasks plugin, its global filter emoji) so a query or grep can isolate them from template placeholders and verification checklists. This is optional — plain `- [ ]` everywhere works fine for a smaller vault; adopt the marker once you have enough notes that "real to-do" vs "scaffolding checkbox" needs disambiguating.

## Linking rules

- Wrap every **entity** (person, project, experiment, topic, source, org) in `[[wikilinks]]` on first mention in a note.
- Use `related:` frontmatter for "see also" connections that aren't inline.
- For a one-way pointer that should show as a backlink, just link it; most markdown knowledge tools (Obsidian, Logseq, etc.) track backlinks automatically — and a `related:` frontmatter link is `grep`-able even without one.
- **Every new note links to at least one existing note at birth** (usually its hub or source note) — this prevents orphans.
- If you keep hub/index notes for each domain (an optional pattern, sometimes called a Map of Content or MOC), everything should be reachable from one within ~2 hops.

## File naming

- Notes: `Title Case With Spaces.md` (wikilink-style tools resolve `[[links]]` to these).
- Daily notes: `YYYY-MM-DD.md` in `Daily/`.
- No special prefixes needed except `00_Meta` (sorts to top).

## Attachments & assets

Notes are **not text-only**. Agents may add **images, diagrams, PDFs, data files (CSV/JSON), and short clips** to illustrate their writing.

- Put attachments in **`assets/`**. Name them descriptively: `benchmark-results-by-config.png`, not `image1.png`.
- Embed in a note with `![[asset-name.png]]` (Obsidian-style) or standard markdown `![alt](assets/asset-name.png)` if you're not using an Obsidian-style renderer.
- A small generated **chart/figure** often illustrates a point better than a wall of numbers — prefer it when it helps.
- **Keep the git repo lean.** Small illustrative assets (images, diagrams, short clips, small data) are fine to commit. For **large/heavy media** do **not** copy into the vault — link to where it already lives (a local path, a URL, a cloud drive), or use git-LFS if it truly must be in-vault.

## The golden rule

**Metadata over location; atomic over monolithic.** A note's folder is a hint; its `type`, `summary`, `tags`, and `links` are what make it findable — and small self-contained notes are what make retrieval sharp. Keep those correct and the graph stays navigable no matter how big it grows.
