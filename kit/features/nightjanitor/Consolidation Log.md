---
type: meta
title: Consolidation Log
summary: "A record of every NightJanitor run: the @mentions it handled, the inbox items it filed, the fixes it made and the items it flagged."
aliases: [Consolidation Log, NightJanitor Log]
created: 2026-07-27
updated: 2026-07-27
tags: [meta, ai/agents]
related: ["[[AGENTS]]", "[[00_Meta/Agent Commands]]"]
---

# Consolidation Log

A record of NightJanitor runs: the `@mentions` it handled, the inbox items it filed, the fixes it made and the items it flagged for you. One dated section per run, newest at the bottom. Never edit past entries.

## Example entry shape (delete once you have real ones)

```
## 2026-07-27 (NightJanitor 23:01)

**@mentions handled**
- `Projects/Example.md` — "@NightJanitor tidy this" → normalized frontmatter, fixed 1 link.

**Mechanical fixes**
- Refreshed `updated:` on 2 touched notes.

**Flagged for you (checklist)**
- [ ] Something ambiguous NightJanitor wouldn't guess at.
```

The prompt this run reads from is in [[00_Meta/Scheduled Agents|Scheduled Agents]].
