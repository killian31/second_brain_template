---
type: meta
title: Second-Brain Agent Skill
created: 2026-07-27
updated: 2026-10-01
tags: [meta, ai/agents]
related: ["[[AGENTS]]"]
---

# Second-brain agent skill

This folder is what tells a new agent session that the vault exists and that it should read from it and write to it. It lives inside the vault, and installing it links or copies it to wherever each tool looks for skills.

## Files

- `SKILL.md` is the skill, in the format Claude Code and Codex use: a markdown file with `name` and `description` in its frontmatter, loaded when a task relates to the user or the vault. It holds the table of `/second-brain` commands.
- `pointer-snippet.md` is a short block for a tool's global instructions file. The tool reads it in every session, so the vault is consulted even when the skill is not triggered.
- `install.sh` installs both for Claude (Code and desktop), Codex and Gemini CLI. You can run it again safely.

The steps of each command are in `../Commands.md`, outside this folder. Kept there, they show up in `INDEX.md` and read the same whichever tool loaded the skill.

## Why there are two pieces

The skill carries the full instructions and loads only when relevant. A tool decides when to load a skill by matching its description against the task, and that match sometimes misses. The pointer covers those cases, because it sits in the instructions the tool always reads.

## Install

```bash
bash 00_Meta/skill/install.sh claude codex gemini   # the tools you name
bash 00_Meta/skill/install.sh                       # every known tool already present on this machine
```

The vault path defaults to the vault the script lives in. Override it with `VAULT=/path`.

For each tool, the script:

1. Writes the real vault path into `SKILL.md`.
2. Links the skill folder into the tool's skills directory, or copies it if linking fails. If a real folder is already there, the script moves it aside as `.bak` and does not delete it.
3. Adds the pointer block to the tool's global instructions file, with `$VAULT` replaced by the real path.

Running it again replaces the block between the `BEGIN` and `END` markers, so the block is never duplicated. Restart the tool after installing, because skills and global instructions are read when a session starts.

## Other agents (Cursor, Copilot, Augment, a custom harness)

The script covers only tools whose skills folder and instructions file are documented, stable paths. For any other tool, the agent reading this does the install. If that is you, you know where your own skills folder and global instructions live, so do these two things:

1. Put `SKILL.md` wherever your tool finds reusable skills, tools or custom instructions. If your tool has no such thing, skip this step. The pointer still works alone, as an always-on instruction.
2. Paste the contents of `pointer-snippet.md`, with `$VAULT` replaced by the real path, into whatever your tool always loads: a system prompt field, a "custom instructions" box, a global rules file.

If the instructions sit behind a settings screen you cannot write to, print the finished snippet and ask the user to paste it. Both files are plain markdown, so nothing needs translating.

These are the usual places for the pointer. Products move these settings around, so trust the tool's current docs over this table.

| Tool | Where the pointer goes |
|---|---|
| Claude Code and Claude desktop | `~/.claude/CLAUDE.md` (done by `install.sh`) |
| Codex | `~/.codex/AGENTS.md` (done by `install.sh`) |
| Gemini CLI | `~/.gemini/GEMINI.md` (done by `install.sh`) |
| Cursor | Settings → Rules → User Rules |
| GitHub Copilot | `.github/copilot-instructions.md` in a repo, or the "custom instructions" setting of your editor for a global one |
| Augment | The User Guidelines / Rules panel |
| Anything else | Whatever the tool always loads: a system prompt, a "custom instructions" box, a global rules file |

## Uninstall

- Remove the `second-brain` folder or link from each tool's skills directory.
- Delete the block between `<!-- BEGIN SECOND-BRAIN -->` and `<!-- END SECOND-BRAIN -->` in each tool's global instructions file.
