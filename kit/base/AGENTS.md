---
type: meta
title: AGENTS
aliases: [AGENTS, Agent Guide, Read Me First, Operating Manual]
summary: The manual every agent reads first. It covers how this second brain is organized, what every note's frontmatter must contain, how to write small linked notes, and how to find things quickly.
created: 2026-07-27
updated: 2026-10-01
tags: [meta/agents, meta/entrypoint]
---

# AGENTS: read this first

> [!important]
> If you are an AI agent working in this vault, read this file at the start of every session. It explains how the vault is organized, the conventions to follow, and how to find things.

This vault is {{YOUR_NAME}}'s second brain: a set of linked notes that agents read, search, extend and connect. It is built so that an agent can find the right note quickly. Every note carries a one-line `summary` and structured metadata, so you can locate and filter information without reading everything. Each note holds one idea, and the vault is meant to contain many small notes with many links between them.

The vault is plain markdown. It needs no database and no particular app, and any agent that can read and write text files and run `python3` can work in it. Optional extras (background agents, git sync, Obsidian) are listed under "Installed features" at the end of this file. If a feature is not listed there, it does not exist in this vault.

## 1. Orientation

1. [[INDEX]] is a flat catalog of every note, grouped by `type`, each with its one-line `summary`. Start here.
2. [[LOG]] is a timeline of what changed in the vault.
3. This file holds the rules. [[00_Meta/Conventions|Conventions]] has the full specification for metadata and note size.

If you are looking for a specific fact, do not browse folders. Search (see §5).

## 2. Folder map

```
INDEX.md                catalog of all notes by type, each with a summary (read this first)
LOG.md                  timeline of vault events, newest at the bottom
Inbox.md                dump anything here; it gets sorted later
AGENTS.md               this file
00_Meta/
  Conventions.md        frontmatter, note size and tag rules (the reference)
  Commands.md           the steps of each /second-brain command
  Templates/            copy these when creating notes
  scripts/              build_index.py (rebuilds INDEX) and lint.py (health check)
About Me/               stable facts about the user: profile, preferences, goals
People/                 one note per person
Orgs/                   one note per organization: employer, company, lab
Experiments/            things tried, from hypothesis to result
Analyses/               syntheses an agent filed after a conversation
Projects/               things being built, with a status; these are hubs that link out to small notes
Decisions/              commitments made and why; binding until reversed
Knowledge/              concept and topic notes; this folder should hold many small notes
Sources/                references: articles, books, papers, links
Ideas/                  raw ideas
assets/                 images, diagrams, PDFs and clips embedded in notes
Daily/                  one note per day (YYYY-MM-DD)
```

Folders only group notes roughly. What makes a note findable is its frontmatter, its summary, its tags and its links, so where a note sits matters less than its metadata.

Once the vault is large, a hub note per domain (a "map of content") helps keep everything within a couple of links. It is an ordinary note that links out, and none is created by default.

## 3. Frontmatter

Every note must begin with YAML frontmatter. The minimum is:

```yaml
---
type: topic              # see allowed values below
title: Short human title
summary: One or two plain-text sentences describing the note, so an agent knows what's inside without opening it.
aliases: []              # synonyms to match in search/links
status: active           # only for experiment/project/idea; else omit
created: 2026-07-27
updated: 2026-07-27
tags: [domain/subdomain]
related: []              # wikilinks to related notes, e.g. ["[[Some Note]]"]
---
```

Allowed `type` values: `meta`, `moc`, `profile`, `experiment`, `project`, `person`, `topic`, `source`, `daily`, `org`, `idea`, `analysis`, `decision`.

Allowed `status` values, for experiments, projects and ideas: `idea`, `active`, `paused`, `done`, `abandoned`.

Two fields matter most:

- `summary` is required. It fills [[INDEX]] and lets an agent judge whether a note is relevant before opening it. Write one or two plain sentences that make sense without the rest of the note. A note with a weak summary is hard for the next agent to find.
- `type` is what every search by category relies on. Do not invent a new `type` value without recording it in [[00_Meta/Conventions|Conventions]].

Two optional fields separate hard facts from synthesis: `provenance` (`stated`, `verified`, `inferred` or `mixed`) and `confidence` (`high`, `medium` or `low`). The full specification, including fields specific to each type and the tag list, is in [[00_Meta/Conventions|Conventions]].

## 4. How to write

- **One idea per note.** A note is what a search returns. A small note about one concept gives a precise result and costs little context. A long note about ten things gives a vague result and fills the next agent's context with text it did not need. Aim for about 100 to 400 words in a `topic` note, and prefer many small linked notes to a few large ones. The tests for when to split are in [[00_Meta/Conventions|Conventions]], under "Note size & atomicity".
- **A project note is a hub.** It may be long, but a concept, a mechanism or a decision that could be cited elsewhere belongs in its own `topic` note in `Knowledge/`, linked from the project. When you add substantial detail to a project, ask whether the idea could be reused. If it could, give it its own note.
- **Split a note that has grown past one idea.** If a section has its own title, or you want to link to part of a note, that part should be a separate note. Create the new `topic` note with its own `summary` and link the two in both directions. Leave the original text in place unless the user agreed to trim it.
- **Write without asking.** Agents maintain this vault for other agents. When a task produces or reveals something worth keeping (a result, a benchmark, a decision, a fact, a preference, a bug, a concept), recording it is the last step of the task. Do not stop to ask "should I write this to the second brain?" Write it, then say that you did. Skip only what is trivial or will not matter tomorrow.
- **File your own answers.** When your answer to the user is a synthesis worth rereading (a comparison, an analysis across several notes, a decision with its reasons, a plan, a connection you found), save it as a `type: analysis` note in `Analyses/`, or append it to the relevant project or person note. Mark it as agent-written with `source: conversation (YYYY-MM-DD)` and `provenance: inferred`, link every entity, and tell the user. Simple lookups do not need filing.
- **Capture small things.** Nothing is too small to log. Put half-formed thoughts, links and one-line facts in [[Inbox]], which needs no frontmatter, or in today's `Daily/` note. Turn the ones worth keeping into proper notes in a later session. If the NightJanitor feature is installed (see §8), it does this every night.
- **Never invent facts about the user.** If you do not know something, leave the field blank or write `// TODO: confirm`. Record only what the user states, what you can verify, or what you clearly mark as inference with `> [!note] Inferred:` and `provenance: inferred`.
- **Link every new note.** A new note needs a `summary` and a link to at least one existing note, usually its source or the nearest hub. This keeps orphans out of the vault and keeps INDEX useful.
- **Use attachments when they help.** Put images, diagrams, PDFs and short clips in `assets/` and embed them with `![[name.png]]` when they make a note clearer, such as a benchmark chart or an architecture diagram. Link to very large media and do not copy it in. The rules are in [[00_Meta/Conventions|Conventions]], under Attachments.
- **Link on first mention.** Wrap every person, project, experiment, topic, source and org in `[[wikilinks]]` the first time it appears in a note.
- **Keep metadata current.** Refresh `updated:` whenever you edit a note, and start new notes from a template in `00_Meta/Templates/`.

### Ask before these actions

You may read, append and create notes freely. Ask the user before you delete a note, restructure folders, rename or move files, or rewrite existing notes in bulk. Adding a new note, or adding a `summary` to a note that lacks one, needs no confirmation.

## 5. How to search

Go from cheap to expensive, and stop as soon as you have enough.

0. Read [[INDEX]]. Scan titles and summaries to shortlist notes without opening them. Use [[LOG]] to see what changed recently.
1. Search by type: grep `type: experiment` (or `project`, `person`, `topic`) to list a category.
2. Search by tag: grep the tag, such as `#learning` or `tags: .*video`.
3. Search by link: grep `[[Note Name]]` to find every note that refers to it.
4. Open the shortlisted notes. Follow their links to repos, papers or data only if you still need more.

In short: INDEX first, then summaries, then the few notes that matter, then the raw sources. Never start from the file tree.

## 6. Commands

The user can drive the vault with a verb in chat: `/second-brain ingest <url>`, `capture`, `save`, `ask`, `research`, `lint`, `reindex`, `review`, `agenda`. The steps of each are in [[00_Meta/Commands|Commands]]. Read that file before running `ingest`, `research`, `lint` or `review`. The commands are shortcuts. The rules above about reading first and writing back apply whether or not a command was used.

## 7. Checklist for a new agent

- [ ] Read this file.
- [ ] Scan [[INDEX]] to see what exists.
- [ ] Skim [[00_Meta/Conventions|Conventions]] if you are going to write.
- [ ] For a task, grep the relevant folder, `type:` or tag.
- [ ] When you add knowledge: one idea per note, a `summary`, links, and a fresh `updated:`.

## 8. Installed features

The optional extras installed in this vault are listed below. If a feature is not listed, it is not installed, so do not assume its files or conventions exist. To add one, ask an agent to follow Phase 3 of `SETUP.md` at https://github.com/killian31/second_brain_template.

<!-- features: one block per installed feature is appended below this line -->
