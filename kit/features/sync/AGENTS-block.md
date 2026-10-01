### Git sync

This vault is a private git repository, synced automatically by **one owner per machine** (`00_Meta/scripts/sync.sh` on a timer, or the Obsidian Git plugin): commit, pull with rebase, push, every few minutes.

- Agents must not run git commands that change the repository. Write notes and let the sync owner commit them. Run git by hand only when the user asks for an immediate sync or a recovery.
- `INDEX.md` is generated and git-ignored: each machine rebuilds it. If it is missing (fresh clone), run `python3 00_Meta/scripts/build_index.py`.
- If the sync log reports an unresolved conflict, resolve it in the affected note keeping both sides, `git add` it, `git rebase --continue`. Never force-push, never discard the other machine's version.
