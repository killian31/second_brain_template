#!/usr/bin/env bash
# Commit, pull (rebase), push the vault, then rebuild the local INDEX.
# Meant to run on a timer, from one or several machines. Installed by the Backup & multi-machine feature (SETUP.md, B1).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."

# Another git process is mid-write: skip this tick, the next one catches up.
[ -e .git/index.lock ] && exit 0
# A previous pull hit a real conflict: stop until someone resolves it, never commit on top.
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
  echo "$(date '+%F %T') sync stopped: unresolved conflict in $(pwd) (git status to see it)" >&2
  exit 1
fi

git add -A
git diff --cached --quiet || git commit -qm "vault sync: $(hostname -s) $(date '+%F %H:%M')"
git pull -q --rebase --autostash
git push -q

# INDEX.md is generated and untracked (two machines rebuilding it would conflict every time).
python3 00_Meta/scripts/build_index.py >/dev/null 2>&1 || true
