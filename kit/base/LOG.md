---
type: meta
title: LOG
aliases: [LOG, Activity Log, Timeline]
created: 2026-07-27
updated: 2026-07-27
tags: [meta/entrypoint]
related: ["[[AGENTS]]", "[[INDEX]]"]
---

# LOG

A timeline of what happened in the vault, one line per entry, newest at the bottom. The next agent reads it to see what changed recently without going through git history.

Format: `## [YYYY-MM-DD] <kind> | <what happened>`, where kind is one of `setup`, `ingest`, `decision`, `build`, `lint`, `review`.

```
## [2026-01-01] ingest | 3 notes from <source>, linked into [[Knowledge/...]]
## [2026-01-02] decision | [[Projects/...]] status active -> done
```

Never edit past entries. This file is a record of what happened.

