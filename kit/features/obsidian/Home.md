---
type: moc
title: Home
summary: "Live Obsidian dashboard (Dataview): active projects, recently updated notes, ideas, latest daily notes and vault stats. Renders only inside Obsidian; agents use INDEX instead."
aliases: [Home, Dashboard]
cssclasses: [home]
created: {{DATE}}
updated: {{DATE}}
tags: [moc, meta/entrypoint]
related: ["[[AGENTS]]", "[[INDEX]]"]
---

# Home

{{YOUR_NAME}}'s second brain. This page updates itself. Dump anything in [[Inbox]]; agents start at [[AGENTS]] and [[INDEX]].

## Active right now

```dataview
LIST
FROM "Projects" OR "Experiments"
WHERE status = "active"
SORT updated DESC
```

## Recently updated

```dataview
TABLE WITHOUT ID file.link AS "Note", type AS "Type", updated AS "Updated"
WHERE type AND type != "meta" AND type != "moc"
SORT updated DESC
LIMIT 12
```

## Ideas to develop

```dataview
LIST
FROM "Ideas"
WHERE type = "idea" AND status = "idea"
SORT created DESC
```

## Latest daily notes

```dataview
LIST
FROM "Daily"
WHERE type = "daily"
SORT file.name DESC
LIMIT 7
```

## People

```dataview
LIST
FROM "People"
WHERE type = "person"
SORT updated DESC
LIMIT 20
```

## Vault stats

```dataview
TABLE WITHOUT ID key AS "Type", length(rows) AS "Notes"
WHERE type
GROUP BY type
SORT length(rows) DESC
```

> [!tip] Empty sections just mean there are no notes of that kind yet. Every note with correct frontmatter shows up here on its own.
