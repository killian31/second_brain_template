---
type: meta
title: Commands — the /second-brain command protocol
aliases: [Commands, Second Brain Commands, Slash Commands]
summary: Full step-by-step protocol for the nine /second-brain commands (ingest, capture, save, ask, research, lint, reindex, review, agenda). The skill's SKILL.md carries the one-line summaries; this note carries the multi-step procedures agents must follow.
created: 2026-07-27
updated: 2026-07-27
tags: [meta/agents, meta/commands]
related: ["[[AGENTS]]", "[[00_Meta/Conventions]]"]
---

# Commands — the `/second-brain` command protocol

> [!important] For agents.
> You can invoke this vault with an explicit verb: `/second-brain <command> <args>`.
> `SKILL.md` lists the commands and their one-line contracts. **This note is the detailed procedure** for the multi-step ones — read it before running `ingest`, `research`, `lint`, or `review`.
> Everything here obeys [[AGENTS]] and [[00_Meta/Conventions|Conventions]]: atomic notes, `summary` on every note, `[[wikilinks]]` everywhere, refresh `updated:`, never invent facts.

## Dispatch rules

- **No argument** (`/second-brain`) → the default behaviour: read `AGENTS.md` + `INDEX.md` and load context relevant to the conversation. Not a command.
- **Unrecognised first word** → do *not* error. Treat the whole argument as a natural-language request and route it to the closest command (usually `ask`).
- **Missing required argument** → ask for it in one line; don't guess.
- Commands are a shortcut, not a gate. Every behaviour here is also available by asking in plain language, and the **automatic** read-context / write-back rules in [[AGENTS]] apply whether or not a command was used.

## Command quick reference

| Command | Argument | Writes? |
|---|---|---|
| `ingest` | url \| pdf \| path \| pasted text | yes — `Sources/` + `Knowledge/` |
| `capture` | free text | yes — `Inbox.md` only |
| `save` | — | yes — `Analyses/` + touched notes |
| `ask` | question | no |
| `research` | topic | yes — `Sources/`, `Knowledge/`, `Analyses/` |
| `lint` | — | **no** (reports; asks before fixing) |
| `reindex` | — | yes — `INDEX.md` only |
| `review` | `weekly` \| `monthly` | yes — one `Analyses/` note |
| `agenda` | — | no |

---

## `ingest <url | pdf | path | pasted text>`

Turn an external source into vault knowledge. **The goal is not to store the article — it's to extract the reusable ideas out of it.**

1. **Fetch.** Retrieve the source. If a web fetch returns a JS shell or boilerplate, re-fetch with browser tools rather than guessing from the fragment. For a paper, read the abstract page *and* the PDF. For a repo, read the README plus the entry points.
2. **Dedupe before writing.** Grep the vault for the URL, DOI, title, and author. If a `type: source` note already covers it, **update that note** — never create a second one. Say so in the report.
3. **Create the source note.** `Sources/<Title>.md` from `00_Meta/Templates/source.md`. Fill `summary` (what it is + the one thing worth remembering), `author`, `url`, `kind`, `tags`. Fill the `## Takeaway` section — one sentence.
4. **Extract atomic notes.** This is the important step. Each *reusable* idea — a concept, mechanism, result, technique, argument — becomes its **own** `type: topic` note in `Knowledge/`, ~100–400 words, with its own `summary`. One idea per note. A paper yielding one 2000-word note has been filed, not ingested.
   - Skip ideas already covered by an existing `Knowledge/` note; instead, **link the source into that note** and add anything genuinely new.
5. **Link both ways.** Every new `Knowledge/` note links to the source note and to ≥1 existing note. The source note's `## Connects to` lists the topics and projects it informs. No orphans.
6. **Flag contradictions, never overwrite.** If the source disagrees with something in the vault, add to the existing note:
   `> [!warning] Contradicted by [[Sources/<Title>]] (2026-07-27): <what differs>`
   Leave the original claim in place. You resolve it later.
7. **Report.** List: source note created/updated · atomic notes created · existing notes linked · contradictions flagged.

**Don't:** paste the full text into the vault; create a `Knowledge/` note without a `summary`; ingest into `Projects/`.

---

## `capture <text>`

The zero-friction path. Speed is the entire feature.

1. Append one bullet to the `## To process` list in `Inbox.md`. No frontmatter, no filing decision, no clarifying question — **even if the text is ambiguous.**
2. If it is unambiguously actionable, write it as a task so it's easy to find later: `- [ ] <text>` (add a due date if one was stated).
3. Keep the trailing empty bullet and the `## To process` heading intact.
4. Confirm in **one line**. Do not summarise, expand, or offer to file it properly.

Never route a `capture` into `Knowledge/`, `Ideas/`, or a project note — that defeats the purpose. If it clearly deserves a real note, capture it *and* say so; let the user decide.

---

## `save`

Flush the current conversation into the vault **now**, mid-conversation, rather than at task end.

> Write-back is already automatic per [[AGENTS]] §4 — this command exists to force it at a chosen moment (before a context reset, or when the durable part just happened but the task isn't over).

1. Identify what's durable: decisions + rationale, results/benchmarks, new facts or preferences, new people/orgs/projects, concepts worth keeping, changed project status.
2. Route each item per [[AGENTS]] §4 — `About Me/`, `Projects/`, `Experiments/`, `Knowledge/`, `People/`, `Orgs/`.
3. If the conversation produced **synthesis** (a comparison, a plan, a decision rationale, a discovered connection), file it as a `type: analysis` note in `Analyses/` from `00_Meta/Templates/analysis.md`, with `source: conversation (2026-07-27)` and `provenance: inferred`. Link every entity.
4. Refresh `updated:` on everything touched.
5. Report the file list. Skip trivia silently — an `Analyses/` note per chat is noise.

---

## `ask <question>`

Answer **from the vault only**. This command's value is that its answers are trustworthy.

1. Tiered retrieval per [[AGENTS]] §5: `INDEX.md` (titles + summaries) → grep by `type` / `#tag` / `[[backlink]]` → open only the shortlisted notes. Stop when you have enough.
2. Answer, **citing the notes used** as `[[wikilinks]]` so the user can verify.
3. If the vault doesn't cover it, **say so plainly** — "the vault has nothing on this" — and offer `research`. Do not quietly fill the gap from model knowledge.
4. If you do add outside knowledge, label it explicitly as outside the vault, in its own paragraph.
5. If two notes disagree, surface **both** and say they conflict. Don't silently pick a winner.
6. Read-only. `ask` writes nothing.

---

## `research <topic>`

**Vault-first research.** The point is to avoid re-researching what's already been concluded, and to catch where the world has moved past your notes.

1. **Read the vault first.** Assemble everything already known on the topic — `Knowledge/`, `Sources/`, `Experiments/`, `Analyses/`. Summarise it back before searching anything.
2. **Name the gaps.** Explicit open questions the vault does not answer. These, and only these, define the search.
3. **Search only the gaps.** Don't re-derive settled ground.
4. **Return a delta**, in exactly these three buckets:
   - **New** — genuinely absent from the vault.
   - **Confirmed** — external sources agree with what's already recorded (cite which note).
   - **Contradicted** — the vault is now wrong or stale. Name the note, quote the claim, give the counter-evidence.
5. **File it:**
   - Each substantive source → a `Sources/` note (see `ingest`, steps 3–5).
   - Each new concept → an atomic `Knowledge/` note.
   - Contradicted notes → append a dated correction block; **do not overwrite** the original claim; bump `updated:`.
   - The delta itself → an `Analyses/` note (`tags: [analysis, meta/research]`), linked to every note it touches.
6. Report the three buckets plus the files written.

---

## `lint`

**Read-only health report. Never auto-fixes.** Report first, then ask which fixes to apply — this mirrors the confirm-before-side-effects rule in [[AGENTS]] §4.

```bash
python3 00_Meta/scripts/lint.py
```

Run this first (from the vault root) — it does the mechanical pass (frontmatter contract, wikilink/alias resolution, orphans, INDEX drift, staleness, oversized notes) in one shot instead of reading every note by hand. Then read its output with judgment before reporting: the script can still false-positive on things it can't know (e.g. a link that *should* exist but doesn't yet, vs. one that's fine as prose) — spot-check anything surprising the way you would any other tool output, don't just relay it verbatim.

**Out of scope** — the script already excludes these; don't re-flag them by hand either:
- `README.md` (vault root), if present — a plain repo readme, not a vault note.
- `00_Meta/**` — tooling/infra (templates, skill, scripts, meta docs), not vault content the frontmatter contract applies to.
- Any generated, plugin-specific dashboard folder you add later (human-facing only) — not hand-maintained.
- `_README.md` folder-doc files — exempt from the orphan check, they document a folder rather than being a retrieval note.
- A `[[wikilink]]` that resolves via the target note's `aliases:` frontmatter, not just its filename/path.

Check, and group findings by severity with file paths and counts:

**Contract violations (high)**
- Missing YAML frontmatter, or missing `type`.
- `type` outside the allowed set: `meta`, `moc`, `profile`, `experiment`, `project`, `person`, `topic`, `source`, `daily`, `org`, `idea`, `analysis`.
- `status` outside `idea` / `active` / `paused` / `done` / `abandoned` on an experiment, project, or idea.
- Missing `summary` — this one matters most; it breaks `INDEX` and all retrieval.

**Retrieval quality (medium)**
- Weak `summary`: empty, under ~8 words, or just restating the title.
- Broken `[[wikilinks]]` — target note doesn't exist.
- Orphans: zero inbound links (exclude `INDEX`, `LOG`, `Home`, any Map/MOC folder, any dashboard folder).
- `INDEX.md` drift: notes on disk missing from the catalog → recommend `reindex`.

**Staleness & hygiene (low)**
- `status: active` project or experiment whose `updated:` is older than ~60 days.
- Missing `updated:`, or `updated:` earlier than `created:`.
- Oversized `topic` notes far past ~400 words, or with multiple `##` sections that each stand alone → **flag as split candidates** so the next agent to edit that note breaks it up. `lint` itself never splits.
- `Inbox.md` backlog older than a few days.

Then: "Fix which of these?" Apply only what the user names. Additive fixes (adding a missing `summary`) are safe; deletions, renames, moves and bulk rewrites always need explicit OK.

If the NightJanitor feature is installed (see [[AGENTS]] §8, Installed features), this overlaps its nightly run on purpose — `lint` is the on-demand version.

---

## `reindex`

```bash
python3 00_Meta/scripts/build_index.py
```

Regenerates `INDEX.md` from `summary:` frontmatter. Report what changed — notes added, notes removed, and any note that fell back to its first body line because it has **no `summary`** (those should get a real one; see `lint`).

Do **not** run mutating git commands unless the user asks — if you use an auto-sync tool (e.g. Obsidian Git) it owns the commit/push cycle; otherwise commit normally when the user wants a snapshot.

---

## `review [weekly | monthly]`

Defaults to `weekly`. A structured look back that **compounds** — each review is filed so the next one can diff against it.

**Read:** `Daily/` notes in the window · the tail of `LOG.md` · `Projects/` with `status: active` · `Experiments/` · `Ideas/` · `Inbox.md` · open tasks · the previous review note in `Analyses/`.

**Produce:**
- **Moved** — what actually progressed, with the evidence (note, result, decision).
- **Stalled** — `status: active` but untouched in the window. Name them; don't soften it.
- **Captured but never processed** — `Inbox.md` backlog, `Ideas/` with no follow-up, sources ingested but never linked into a project.
- **Decided** — decisions made in the window and their rationale.
- **Next** — a short priority list, tied to `About Me/Goals.md` if you keep one.
- *(monthly only)* — roll up the weekly reviews; check progress against goals; flag any goal with no active project behind it.

**File it** as a `type: analysis` note in `Analyses/` — `Analyses/Review YYYY-Www.md` (weekly) or `Analyses/Review YYYY-MM.md` (monthly), `tags: [analysis, meta/review]` — linked to every project and person it discusses.

---

## `agenda`

What's actually due. Read-only, writes nothing.

1. Collect open tasks across the vault (however you mark them — see [[00_Meta/Conventions#Tasks]]).
2. Also scan `Projects/` frontmatter and bodies for stated deadlines and milestones.
3. Output grouped: **Overdue** · **Today** · **This week** · **Later** · **Undated** (committed but never scheduled — the easiest thing to lose).
4. Order by priority within each group, and link each item back to its note.
