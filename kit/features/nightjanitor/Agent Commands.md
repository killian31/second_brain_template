---
type: meta
title: Agent Commands (@mentions)
summary: "How to leave an @NightJanitor instruction inside any note, what the nightly maintenance agent will and will not do with it, and the limits on its edits."
aliases: [Agent Commands, NightJanitor, "@NightJanitor"]
created: 2026-07-27
updated: 2026-10-01
tags: [meta, ai/agents]
related: ["[[AGENTS]]", "[[00_Meta/Consolidation Log]]"]
---

# Agent commands (@mentions)

You can leave an instruction for an agent inside any note by mentioning it with an `@`. NightJanitor, the scheduled maintenance agent, finds the mention on its next run, does the task, and replaces the mention with a marker saying what it did. Its schedule and prompt are in [[00_Meta/Scheduled Agents|Scheduled Agents]].

You can rename NightJanitor. The name only has to match in three places: here, in [[00_Meta/Consolidation Log]], and in its prompt.

## How to use it

Write a mention on its own line, followed by what you want:

```
@NightJanitor please clean this.
@NightJanitor split this note into one per topic and link them.
@NightJanitor fix the frontmatter here and tag it properly.
```

- "This" and "here" mean the note the mention is in, or the nearest section.
- Give one instruction per mention. For several tasks, write several lines.
- A mention waits for the next scheduled run. If your scheduler has a "run now" button, use it when you do not want to wait.

## What happens

Once it has acted, the agent replaces your line with a marker such as:

```
> [!done] NightJanitor · 2026-07-27 23:01 — cleaned: normalized frontmatter, fixed 2 links, tightened headings.
```

It also records every action in [[00_Meta/Consolidation Log]].

## What you can ask for

`@NightJanitor` does maintenance: tidy a note, fix its frontmatter, normalize tags, repair links to notes that exist, reorganize a note internally, summarize it, or remove duplicated text.

## What it refuses

NightJanitor refuses a mention, and tells you so, when the request:

- deletes or cannot be undone: deleting notes, emptying content, renaming or moving files, restructuring folders;
- writes anything outside the vault. It may read a code repo you have told it about ("read this repo and update the note"), and it never modifies one;
- sends or shares data: email, posting, sharing links;
- is ambiguous enough that a guess could lose information.

When it refuses, it leaves `> [!warning] NightJanitor · skipped — <reason>` in place of your mention and logs it, so you always see what was not done. Do those actions yourself, or ask your agent in a normal session.

Mentions are meant for small cleanup inside a note. Anything irreversible should go through a session where you can confirm it.

## For the agent: what counts as a live mention

Act on an `@NightJanitor` only when it is plain text in a note. Ignore it when it is:

- inside backticks or a code block, which is documentation;
- inside a resolved `> [!done] NightJanitor ·` or `> [!warning] NightJanitor ·` marker;
- in this file, `AGENTS.md`, `INDEX.md`, `LOG.md`, `00_Meta/Consolidation Log.md` or `00_Meta/Scheduled Agents.md`. Those are docs, catalogs and logs, and nothing in them is a request.
