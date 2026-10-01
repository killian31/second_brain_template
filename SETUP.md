# Setting up a second brain

You are an AI agent, and your user asked you to set up a second brain from this repo. This file is your script. Follow it from top to bottom.

Act like a friend who already uses this system and is sitting next to the user. Keep messages short and warm, and avoid jargon unless they use it first.

This repo is a kit. Do not clone it into the user's folder. You build their vault in the folder they choose, from their answers: a small base that everyone gets, then only the features they tick. `kit/base/` and `kit/features/` hold the files you copy from, so that conventions, scripts and prompts are copied exactly and never rewritten from memory.

Ground rules:

- Go one step at a time. Ask, wait, act, say in one line what you did, then move on. Never send all the questions at once.
- Speak the user's language, whatever language this file is in.
- Every question can be skipped. "Skip" and "later" are valid answers. If you do not know something, leave the field empty and do not guess.
- Offer a default with every question, so that "yes" is always enough.
- If you have a multiple-choice or checkbox question tool, use it for every level of the menu in Phase 3. If you do not, print a numbered list and let them answer with numbers.
- You need local file access. If you are a browser chat with no filesystem, stop and say so. This needs a desktop or command-line agent such as Claude Code, the Claude desktop app, Codex, Gemini CLI or Cursor.
- Ask before you install software, touch an account or create a remote repo. Creating folders and notes inside the vault folder needs no confirmation.

## Phase 0: say what is about to happen

Tell the user, in three or four sentences:

- A second brain is a folder of small linked notes. You read it at the start of every session and add to it on your own, so they stop repeating themselves in each new conversation.
- Setup is a few questions, a base install, and then a menu of extras.
- Nothing leaves their machine unless they choose the backup feature.

Then ask if they are ready.

## Phase 1: interview

Ask five questions, one message each.

1. **Name.** "What should I call you in the notes?"
2. **Location.** "Where should the folder live?" The default is `~/Second_Brain`. If the path already exists and has content, ask before using it. The default avoids `~/Documents` because on macOS that folder is often synced by iCloud and closed to background jobs, which breaks the sync and scheduled features. Use it if they insist.
3. **Language** of the notes. The default is the language they are writing to you in.
4. **About them.** "Tell me a bit about yourself: what you do, what you're working on right now, anything you'd want every future assistant to already know. As much or as little as you like." Let them talk. Ask at most one follow-up, such as "Any people or projects I should know by name?"
5. **Intended use.** "What do you mainly want this for?" Offer examples: work projects and decisions, research and reading notes, personal admin, learning a subject, a journal, or all of it.

Keep their answers word for word. You turn them into notes in Phase 2.

## Phase 2: base install (everyone)

`VAULT` is the path they chose. `KIT` is a temporary copy of this repo.

**2.1 Fetch the kit** into a temporary folder, never into the vault:

```bash
git clone --depth 1 https://github.com/killian31/second_brain_template.git /tmp/sb-kit
```

Without git:

```bash
curl -L https://github.com/killian31/second_brain_template/archive/refs/heads/main.zip -o /tmp/sb-kit.zip
unzip -q /tmp/sb-kit.zip -d /tmp && mv /tmp/second_brain_template-main /tmp/sb-kit
```

If you are reading this file from a local copy of the repo, that copy is your `KIT`.

**2.2 Create the vault.**

```bash
mkdir -p "$VAULT" && cp -R "$KIT/kit/base/." "$VAULT/"
```

The vault now contains:

```
AGENTS.md      the manual every agent reads first
Inbox.md       a place to dump anything
LOG.md         a timeline of changes
00_Meta/       Conventions.md, Commands.md, Templates/, scripts/ (build_index.py, lint.py), skill/
About Me/ People/ Orgs/ Projects/ Decisions/ Knowledge/ Sources/ Ideas/ Analyses/ Experiments/ Daily/ assets/
```

Use their answer to question 5 to fit the folders to them. If their use plainly needs a folder the base lacks (`Recipes/`, `Courses/`, `Journal/`), add it with a one-line `_README.md` and a line in the folder map of `AGENTS.md`. Notes in a new folder are still `topic` or `source`, so do not invent a new `type:`. Do not remove base folders. The conventions refer to them, and an empty folder costs nothing.

**2.3 Personalize.**

- Replace `{{YOUR_NAME}}` in `AGENTS.md` with their name.
- If the notes are not in English, add this line under the title of `AGENTS.md`: `> Notes in this vault are written in <language>.` Leave the meta docs in English.

**2.4 Write the first notes** from the interview. Follow `00_Meta/Conventions.md`: frontmatter, a `summary:` on every note, one idea per note, `provenance: stated`. Record only what they said.

- `About Me/Profile.md` (`type: profile`): who they are and what they do.
- `About Me/How I use this second brain.md` (`type: profile`): their answer to question 5. In Phase 3 you add the list of installed features here.
- One `Projects/<name>.md` per project they named, with `status: active`. Leave `started:` and `target:` empty unless they gave dates.
- One `People/<name>.md` per person, and one `Orgs/<name>.md` per employer, school, client or company.
- Any preference they volunteered, as a small `type: profile` note in `About Me/`.
- Today's `Daily/YYYY-MM-DD.md`, with one line saying the second brain was set up and linking the notes above.
- One line in `LOG.md`: `## [YYYY-MM-DD] setup | vault created, <n> notes seeded`.

Use the templates in `00_Meta/Templates/`. There is no template for `profile` or `org`, so use the minimum header from Conventions. Link the notes to each other with `[[wikilinks]]`. Do not pad: three accurate notes are enough.

**2.5 Install the skill.** The skill is what makes later sessions read and write the vault.

1. Detect the AI tools on this machine. Look for `~/.claude`, `~/.codex`, `~/.gemini`, `~/.cursor` and `~/.copilot`, for the commands `claude`, `codex`, `gemini`, `cursor` and `code`, and for the apps (Claude, Cursor, Antigravity, VS Code with Copilot). You are one of these tools yourself.
2. Ask which ones to install for, as checkboxes. Tick the detected tools in advance, then ask "Any other tool you use?" and offer Claude Code or Claude desktop, Codex, Gemini CLI, Antigravity, Cursor, GitHub Copilot, and "other". Explain what installing does: it appends one marked block to each tool's global instructions file, and links the skill where the tool has a skills folder.
3. Install. A script handles Claude, Codex and Gemini CLI. Name only the tools they ticked:
   ```bash
   bash "$VAULT/00_Meta/skill/install.sh" claude codex
   ```
   For any other ticked tool, do the same two things by hand, following "Other agents" in `00_Meta/skill/README.md`. Check that tool's current docs first for where its global instructions and skills live. If they sit behind a settings screen, print the finished snippet and tell the user exactly where to paste it.
4. Let the tools write to the vault from other folders. The user will mostly work inside other projects, and most tools ask for permission before writing outside the current project, which would mean a prompt for every note. Ask the user whether to add the vault to the folders each tool may read and write without asking, and explain the trade: an agent working in any project can then add notes there with no prompt. In Claude Code this is `permissions.additionalDirectories` in `~/.claude/settings.json` (merge with what is there), plus an allow rule for edits in the vault if they want no prompt at all. For other tools, check their current docs for the equivalent.
5. Remember for Phase 4 that each tool needs a restart before it sees the skill.

**2.6 Check the result.** Run `python3 --version` first. The two scripts need Python 3 and nothing else. If Python is missing, say so and offer to install it. Until then, write `INDEX.md` by hand in the same format, one line per note in the form `- [[Title]] — summary`, grouped by `type`.

```bash
cd "$VAULT" && python3 00_Meta/scripts/build_index.py && python3 00_Meta/scripts/lint.py
```

Fix whatever lint reports. Show the user the notes you created, read the Profile summary back to them, and ask if anything is wrong.

Tell them the base is complete and usable before you move on.

## Phase 3: feature menu

Say: "The base is working. Now the extras. Pick any, none, or come back to them later."

The menu is a tree. Ask the three top-level questions first, as checkboxes. For each one they tick, open its branch and ask about its sub-features, again as checkboxes. Go a level deeper only where a sub-feature is ticked, and never ask about a branch whose parent was declined. A user who wants the minimum answers three questions.

```
A. Background agents: the vault feeds and tidies itself on a schedule
   ├─ A1. NightJanitor          nightly cleanup, and acts on @NightJanitor lines left in notes
   ├─ A2. Morning sync          the last 24 hours of your tools, written into today's note, projects and tasks
   │       └─ which sources?    only the ones that are connected: mail, calendar, drive, chat
   ├─ A3. Weekly review         what moved, what stalled, what is overdue
   └─ where do they run?        on this computer (it must be on), or in the cloud (needs B)

B. Backup and other machines: a private GitHub repo with full history; also lets the agents in A run in the cloud
   ├─ B1. Automatic sync        pull and push every 5 minutes
   └─ B2. Another computer      set up a second machine on the same vault

C. Obsidian: a free app for browsing the vault yourself (agents do not need it)
   ├─ C1. Home dashboard        a live home page: active projects, recent notes, ideas
   │       ├─ C1a. Open on startup
   │       └─ C1b. Open-tasks panel
   ├─ C2. Graph colours         colour the graph by note type
   └─ C3. Sync from Obsidian    (only with B) the Obsidian Git plugin in place of the B1 job
```

With each question, give the one-line description and a recommendation based on the interview. Ask about B before A when you can, because B decides whether the agents in A may run in the cloud.

Reasonable defaults: A1, B and B1 suit almost everyone. A2 suits people whose work happens in mail and chat. C suits people who want to look at their notes, and C1 is worth offering if they sounded keen on C. A3 suits people who want a regular look back at their week.

Install in the order B, A, C, using the sections below. Each feature has the same three parts. Copy its files from `kit/features/<name>/`. Append its `AGENTS-block.md` to the end of the vault's `AGENTS.md`, under "Installed features", which is how later agents learn that the feature exists. Then follow its steps. After each one, tell the user in one line what is now switched on.

When you finish, write the list of installed features, with their times and sources, into `About Me/How I use this second brain.md`, and run 2.6 again.

### A. Background agents

Copy `kit/features/agents/Scheduled Agents.md` to `00_Meta/` and follow the `SETUP` comment at its top: remove the agents they did not tick, fill in the placeholders, delete the comment. Append `kit/features/agents/AGENTS-block.md` to `AGENTS.md`.

A1 needs two more files in `00_Meta/`: `kit/features/nightjanitor/Agent Commands.md` and `Consolidation Log.md`. Also append `kit/features/nightjanitor/AGENTS-block.md` to `AGENTS.md`.

Then, for each ticked agent:

1. Ask what time it should run and write the answer on the agent's `Schedule:` line. Defaults: A1 at 23:00, A2 at 08:00, A3 on Friday at 16:00.
2. For A2 only, choose the sources. Check which connectors or integrations you have (mail, calendar, drive, Slack, Notion, a ticket tracker) and offer only those, as checkboxes. If they want a source that is not connected, tell them where to connect it in their agent's settings and leave it out for now. You cannot authorize it for them. Then write `{{SOURCES}}` as one bullet per source, each with a concrete hint:
   - `- Mail: messages from the last day, skipping promotions and social; open linked meeting notes.`
   - `- Calendar: today's and yesterday's meetings, for context.`
   - `- Slack: direct messages and mentions; read threads for context.`

   Ask whether any channel, sender or project deserves special attention, and add it. Tell them plainly that this agent reads their mail and messages, changes nothing there, and writes only into the vault.
3. Decide where it runs. If B is on, offer both options and recommend the cloud for A1 and A3.
   - In the cloud (needs B): a scheduled agent hosted by their AI platform, such as a Claude Code routine, clones the private repo, does the job and pushes. It runs with the laptop closed. It needs access to the private repo, and A2 also needs the same connectors enabled for the cloud agent. The user grants both. Use the `cloud` value of `{{GIT}}`. Their computer receives the changes at its next sync (B1).
   - On this computer: use the agent app's own scheduled-task feature if it has one, such as Scheduled tasks in the Claude desktop app. If it has none, use `launchd` on macOS, a `systemd --user` timer or `cron` on Linux, or Task Scheduler on Windows, and have it run your own command-line agent non-interactively with the prompt saved to a file (`claude -p`, `codex exec`, `gemini -p`). Use your harness's real flag and a permission mode that lets it write files unattended. A local schedule fires only while the computer is awake and the app is running. A missed run does no harm, because the next run covers the gap. Use the `local` value of `{{GIT}}`.

   Without B the cloud is not an option, because a cloud run cannot see a local folder.
4. Create the schedule with the finished prompt, record the time and place on the agent's `Schedule:` line, and offer to run it once now so they can see the result.

Tell them two more things: each run uses their plan's quota, and Morning sync can see whatever they can see in the tools it reads.

### B. Backup and other machines

1. Check `git --version` and `gh auth status`. If they have no GitHub account or `gh` is not logged in, explain what is missing and how to fix it (`https://github.com/signup`, then `gh auth login`, which they run themselves). Come back to this branch afterwards.
2. Check `git config user.name` and `git config user.email`. If either is empty, ask for it and set it inside the vault repo with `git -C "$VAULT" config ...` once the repo exists.
3. Ask for a repo name (default `second-brain`) and confirm the word "private" with them. This folder will hold personal information.
4. Create the repo and push:
   ```bash
   cd "$VAULT" && git init -q -b main && git add -A && git commit -qm "Initial vault"
   gh repo create <name> --private --source . --push
   ```
   Without B1, they now have a backup that they update by asking you to "sync my second brain".
5. Append `kit/features/sync/AGENTS-block.md` to `AGENTS.md`. Without B1, replace its first paragraph with: "This vault is a private git repository. Nothing syncs automatically: commit and push when the user asks."

**B1. Automatic sync.** Copy `kit/features/sync/sync.sh` to `00_Meta/scripts/sync.sh` and make it executable. The script commits, pulls with rebase, pushes and rebuilds the index, and it is safe to run from several machines. Run it once by hand and check that it exits with 0. Then schedule it every 5 minutes:

- macOS: write `~/Library/LaunchAgents/com.secondbrain.sync.plist` with `Label` set to `com.secondbrain.sync`, `ProgramArguments` set to `/bin/bash` and `<VAULT>/00_Meta/scripts/sync.sh`, `StartInterval` set to `300`, and both `StandardOutPath` and `StandardErrorPath` set to `<home>/Library/Logs/second-brain-sync.log`. Use absolute paths, because launchd does not expand `~`. Then run `launchctl bootstrap gui/$(id -u) <plist>`.
- Linux: a `systemd --user` service and timer with `OnUnitActiveSec=5min`, plus `loginctl enable-linger $USER` if it should run while they are logged out. The fallback is a `crontab` line: `*/5 * * * * <VAULT>/00_Meta/scripts/sync.sh`.
- Windows: Task Scheduler, every 5 minutes, running the script through Git Bash.

Wait for one scheduled run and check that it worked. The script prints nothing on success, so look for an empty log and a fresh commit on GitHub after you edit a note. Errors go to the log. On macOS, background jobs cannot read a vault under `~/Documents`, `~/Desktop` or `~/Downloads` until the user grants access in System Settings → Privacy & Security.

Tell the user two things. Conflicts are rare and never silent: if two machines edit the same line, the sync stops and logs it, and they can ask any agent to "resolve the vault sync conflict". And `INDEX.md` is not synced, because each machine rebuilds its own.

**B2. Another computer.** On that machine, run `gh repo clone <name> <VAULT>`, then do 2.5 (the skill), run `python3 00_Meta/scripts/build_index.py`, and do B1 (the sync job). If the other machine is not at hand, write these steps into `About Me/How I use this second brain.md` so that an agent there can do it later.

### C. Obsidian

1. Install it, after asking. On macOS with Homebrew: `brew install --cask obsidian`. On Windows: `winget install Obsidian.Obsidian`. Otherwise send them to `https://obsidian.md/download`.
2. Configure it in advance so that it works when first opened. Write these files in `$VAULT/.obsidian/`:
   - `app.json`: `{"attachmentFolderPath": "assets", "newFileLocation": "folder", "newFileFolderPath": "Knowledge", "alwaysUpdateLinks": true}`
   - `daily-notes.json`: `{"folder": "Daily", "format": "YYYY-MM-DD", "template": "00_Meta/Templates/daily"}`
   - `templates.json`: `{"folder": "00_Meta/Templates"}`
3. Append `kit/features/obsidian/AGENTS-block.md` to `AGENTS.md`.
4. Have them open it: launch Obsidian, choose *Open folder as vault*, and pick the vault folder. They make this click themselves the first time.
5. Show them three things, in one line each: the graph view in the left ribbon, the quick switcher (Cmd or Ctrl+O) for jumping to any note, and `Inbox.md` as the place to dump anything.

C1, C1a, C1b and C3 need community plugins, which you cannot enable. The user opens *Settings → Community plugins → Turn on community plugins → Browse*, then installs and enables each plugin you name. List every plugin their ticked sub-features need and walk them through it once, so they do it in one go.

**C1. Home dashboard.** Needs the Dataview plugin.

- Copy `kit/features/obsidian/Home.md` to the vault root. Replace `{{YOUR_NAME}}` and `{{DATE}}` (today, as `YYYY-MM-DD`).
- Copy `kit/features/obsidian/home.css` to `.obsidian/snippets/home.css`. Enable it by setting `"enabledCssSnippets": ["home"]` in `.obsidian/appearance.json`. Merge with what is already there, or create the file if it is missing.
- Have them open `Home` in reading view. If a section shows raw `dataview` code, Dataview is not enabled yet.
- Remove the sections for folders this vault does not have, and offer to add one for something they care about. It is their page.

**C1a. Open on startup.** Needs the Homepage plugin. Once they have enabled it, set *Settings → Homepage → Homepage* to `Home` and the view to *Reading view*.

**C1b. Open-tasks panel.** Needs the Tasks plugin.

- Insert this into `Home.md`, before "Vault stats":
  ````
  ## Open tasks

  ```tasks
  not done
  group by filename
  hide backlinks
  ```
  ````
- Have them set *Settings → Tasks → Global task filter* to `#task`. From then on a real to-do is written `- [ ] ... #task`, and a plain `- [ ]` is a checklist item that stays off the panel. Record this in `00_Meta/Conventions.md` under "Tasks (optional convention)". If A2 is on, add "tag each task `#task`" to the Morning sync prompt, both in `00_Meta/Scheduled Agents.md` and in the schedule itself.

**C2. Graph colours.** Needs no plugin. Write `.obsidian/graph.json` with a `colorGroups` array holding one entry per content folder in this vault, each with its own colour. An entry looks like `{"query": "path:Projects", "color": {"a": 1, "rgb": 5431378}}`, where `rgb` is the colour as a decimal integer. If the file exists, merge into it.

**C3. Sync from Obsidian.** Only with B, and in place of B1 on this machine, because each machine should have a single committer. Needs the Obsidian Git plugin. Set the auto commit-and-sync interval to 5 minutes, turn on pull on startup, and set the sync method to *rebase*. It syncs only while Obsidian is open, whereas B1 runs regardless.

## Phase 4: hand over

Rebuild the index and run lint one last time. If you fetched the kit into a temporary folder in 2.1, delete it. Never delete a copy the user already had.

Then explain the system, because the user has not seen it work yet. Send short messages in this order, and stop for questions.

1. How it works. "From now on, when a session starts I read your vault: who you are, your projects, what you've decided. When our work produces something worth keeping, I write it down without asking. You don't have to manage it, or even look at it."
2. Why it improves with use. "It grows out of the work you do with me. The more real work you do through an agent (planning, writing, research, decisions, debugging), the more gets recorded and the less you repeat yourself. If you ask me something in a plain chat with no file access, nothing is saved."
3. What you write and what you never do. Notes are small, one idea each, and linked. You never invent facts about them, and you ask before deleting or reorganizing anything.
4. How to call it. In a tool with slash commands they type `/second-brain <command>`. Anywhere else, plain words work the same way: "second brain: capture ..." or "save this to my second brain". Without any command, the reading and writing still happen.
5. The nine commands. Show the table and say they will mostly use the first four.

   | Command | Use it when |
   |---|---|
   | `capture <thought>` | You want to save something in one line and move on. It goes to the Inbox. |
   | `ingest <url, file or text>` | You read or received something worth keeping, such as an article, a paper, a PDF or meeting notes. It becomes a source note plus one small note per idea. |
   | `ask <question>` | You want an answer from your own notes only, with the notes cited and the gaps admitted. |
   | `save` | The conversation produced something worth keeping and you want it filed now. |
   | `research <topic>` | You want me to check what the vault already knows, search for the rest, and tell you what is new, confirmed or contradicted. |
   | `review weekly` or `monthly` | You want to see what moved, what stalled and what is overdue. |
   | `agenda` | You want your open tasks and deadlines, by urgency. |
   | `lint` | You want a health check: broken links, orphan notes, missing summaries. It changes nothing. |
   | `reindex` | You edited notes by hand and want the index rebuilt. |

6. What is installed. Say where the folder is, which features are on, and when and where each one runs (this computer or the cloud). Add that they can get any skipped feature later by saying "add the <feature> feature to my second brain".
7. The restart. "Quit and reopen <each tool the skill was installed for> once. The skill and the instructions load when a session starts. This conversation already knows about the vault, and new ones will after the restart." If they use Claude, tell them `/second-brain` shows up in the slash menu after the restart.
8. A first real use, now. "Paste me a link you've been meaning to read, or tell me about something you decided this week."

## Adding a feature later

If the user comes back and says "add the <feature> feature", read "Installed features" in the vault's `AGENTS.md` to see what is already there, fetch the kit (2.1), and run only that feature's section.
