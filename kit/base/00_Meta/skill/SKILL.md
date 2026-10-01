---
name: second-brain
description: An agent-maintained second brain — a connected knowledge vault of plain markdown notes about the user's life, preferences, and projects. Use at the START of any session and whenever a task touches the user's background, preferences, goals, people, ongoing work, or past decisions — read it before assuming you lack context. ALSO, and just as importantly, RECORD durable new information into it AUTOMATICALLY as the final step of any task (results, benchmarks, decisions, facts, preferences, new concepts) — do NOT ask permission to write, just do it. Write ATOMIC notes (one idea per note) with a one-line summary. Supports explicit commands — ingest, capture, save, ask, research, lint, reindex, review, agenda — invoked as "/second-brain <command> <args>". If unsure whether something is already known, check the second brain first.
argument-hint: "[ingest|capture|save|ask|research|lint|reindex|review|agenda] <args> — optional; with no argument, just load vault context"
---

# Second Brain

The user keeps an **agent-maintained** knowledge vault — their "second brain" — as a connected graph of Markdown notes. **It is the canonical place for what's known about the user and their work, written by agents for agents.** Read from it before acting, and **write to it automatically** — without asking — whenever a task yields something durable.

## Where it is

**Vault path:** `$VAULT`

`install.sh` stamps the real path on the line above; `$VAULT` below means that path. If it still reads `$VAULT`, the vault root is two folders above this file.

The vault's own operating manual is **`AGENTS.md` at the vault root**. It is the source of truth for structure and conventions — **read it first**; this skill only tells you the vault exists and how to use it day to day.

## Commands

Invoke this skill with an explicit verb: **`/second-brain <command> <args>`**. Commands are a shortcut, never a gate — the automatic read-context and write-back behaviour below applies whether or not one was used, and every command is also reachable by asking in plain language.

| Command | Contract |
|---|---|
| **`ingest <url \| pdf \| path \| text>`** | Turn a source into knowledge: dedupe, write a `Sources/` note, then **extract each reusable idea as its own atomic `Knowledge/` note**, linked both ways. Flag contradictions with existing notes instead of overwriting them. |
| **`capture <text>`** | Zero friction. One bullet appended to `Inbox.md`, no frontmatter, **no clarifying question even if ambiguous**, one-line confirmation. |
| **`save`** | Flush this conversation to the vault *now* (mid-conversation) instead of at task end: durable items routed to their notes, real synthesis filed as a `type: analysis` note in `Analyses/`. |
| **`ask <question>`** | Answer **from the vault only**, citing the notes used. If the vault doesn't cover it, say so plainly and offer `research` — never quietly fill the gap from model knowledge. Read-only. |
| **`research <topic>`** | **Vault-first**: read what's already known, name the gaps, search *only* those, then return a **New / Confirmed / Contradicted** delta and file the results. Stops re-researching settled ground and catches stale notes. |
| **`lint`** | Read-only health report — missing `summary` or `type`, broken wikilinks, orphans, stale `active` notes, INDEX drift, oversized notes. **Reports first, asks before fixing anything.** |
| **`reindex`** | `python3 $VAULT/00_Meta/scripts/build_index.py` → regenerate `INDEX.md`; report the diff. |
| **`review [weekly\|monthly]`** | What moved · what stalled · what was captured but never processed · decisions · next priorities. Filed to `Analyses/` so reviews compound. |
| **`agenda`** | Open tasks and deadlines grouped Overdue / Today / This week / Later / Undated. Read-only. |

**Dispatch:** no argument → just load context as usual (not a command). Unrecognised first word → **don't error**; treat the whole argument as natural language and route it to the nearest command, usually `ask`. Missing required argument → ask for it in one line.

> **Before running `ingest`, `research`, `lint`, or `review`, read `$VAULT/00_Meta/Commands.md`** — it holds the step-by-step protocol for each. The table above is only the contract.

## When to READ it (do this proactively)

At the start of a session, or whenever a task involves:
- Who the user is, their preferences, or how they like work done → `About Me/`
- Their goals → `About Me/Goals.md`, if present
- Any of their projects → `Projects/`
- A topic they've studied → `Knowledge/`
- People in their life → `People/`
- "What did we decide / try before?" → search experiments, projects, and daily notes

**How to find things fast — tiered retrieval (cheap → expensive, stop when you have enough):**
1. Read `$VAULT/INDEX.md` — a flat catalog of every note by `type`, each with a one-line `summary`. Scan titles + summaries to shortlist notes **without opening them**.
2. Grep by metadata: `type: project`, `type: topic`, a `#tag`, or a `[[Note Name]]` backlink.
3. Open only the shortlisted notes; follow their links to raw sources (repos/papers) last.

> Before telling the user you don't have context about them, **check here**. The answer may already be written down.

## When to WRITE to it

**This is automatic, not a question to ask.** Recording durable output is part of finishing a task — never end a task by asking whether to log it; just log it, then mention that you did. Only skip when the info is trivial or ephemeral.

After a task or conversation, record anything **durable** that future-you would want:
- New facts/preferences the user states → update `About Me/` (and set `updated:`).
- A project's progress, decision, or result → update that `Projects/` note.
- Something tried with an outcome → an `Experiments/` note (hypothesis → result).
- A concept worth keeping → an **atomic** `Knowledge/` topic note.
- **A durable answer YOU produced** (a comparison, multi-note synthesis, decision rationale, or plan) → **file it back** as a `type: analysis` note in `Analyses/` (mark it agent-derived with `source: conversation (date)`, `provenance: inferred`), so it compounds instead of vanishing into chat. Bar: real synthesis worth re-reading, not trivial lookups.
- Fleeting thoughts/ideas → **`Inbox.md`** (zero friction, no frontmatter) or today's `Daily/YYYY-MM-DD.md`, then promote durable ones into proper notes.
- **Illustrative media** (a chart, diagram, screenshot, PDF, short clip) → drop it in `assets/` and embed with `![[name.png]]`. Notes aren't text-only. *Link* (don't copy) very large media to keep the git repo lean.

## Write ATOMIC notes (this is the core discipline)

A note is a **retrieval unit**. One small, self-contained note about **one idea** produces a sharp search hit and loads little context; a big note about ten things produces a fuzzy hit and wastes the next agent's context window. So:

- **One concept per note**, ~100–400 words for a `topic` note. Prefer **many small linked notes over few large ones.** If a note needs "and"/a list in its title, it's probably two notes.
- **Self-contained but linked** — each note stands alone when retrieved in isolation, *and* links out with `[[wikilinks]]`.
- **Every note gets a `summary:` frontmatter field** (1–2 plain sentences) — this is what the INDEX and the next agent read first. No summary = hard to find.
- **Projects are hubs, not dumping grounds** — put reusable detail (a concept, mechanism, decision worth citing) in its own atomic `Knowledge/` note and link it from the project.
- **Splitting is additive** — to break up a big note, create the child atomic notes and link both ways; don't delete the original text unless the user approved slimming it.

Follow the vault's rules (full spec in `AGENTS.md` → `00_Meta/Conventions.md`):
- Every note starts with YAML frontmatter incl. `type` and `summary`.
- Copy a template from `00_Meta/Templates/` when creating notes.
- **Link entities** with `[[wikilinks]]`; the graph is the point.
- Refresh `updated:` on every edit.

## Hard rules

- **Never invent facts about the user.** Record only what they state, what you verify, or clearly-marked inferences (`> [!note] Inferred:`, `provenance: inferred`). Empty fields beat plausible fiction.
- **Reading, appending, and creating new notes are fine to do freely.** Deleting notes, restructuring folders, renaming/moving files, or bulk-rewriting existing notes → confirm with the user first.
- Respect privacy: `People/` holds real personal data — store only what's useful and what the user is comfortable keeping.
- If the vault uses the optional `@NightJanitor` mention convention (see `$VAULT/00_Meta/Agent Commands.md`), treat a live mention as an inline instruction, not a broken link or stray text — and never resolve one yourself unless you *are* the scheduled run it's addressed to.

## One-line habit

Start by reading `$VAULT/AGENTS.md` and scanning `INDEX.md`; end by writing back anything durable you learned as an **atomic note with a summary**, linked into the graph.
