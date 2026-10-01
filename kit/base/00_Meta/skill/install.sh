#!/usr/bin/env bash
# Installs "second-brain" awareness into agent tools: a discoverable skill
# (where the tool has a skills folder) + an always-on pointer in the tool's
# global instructions file, so every new session knows the vault exists.
#
# Usage:
#   VAULT=~/Second_Brain ./install.sh claude codex gemini   # the tools you name
#   VAULT=~/Second_Brain ./install.sh                       # every known tool already present on this machine
#
# Known tools: claude (Claude Code / Claude desktop), codex, gemini (Gemini CLI).
# Anything else (Cursor, Copilot, …): see "Other agents" in README.md here.
# Idempotent: re-running refreshes the injected blocks and the skill link.
set -euo pipefail
shopt -u patsub_replacement 2>/dev/null || true   # bash >= 5.2: keep '&' in paths literal

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT="${VAULT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"   # default: the vault this script lives in
VAULT="${VAULT/#\~/$HOME}"
SNIPPET="$SCRIPT_DIR/pointer-snippet.md"
BEGIN="<!-- BEGIN SECOND-BRAIN -->"
END="<!-- END SECOND-BRAIN -->"

note() { printf '  %s\n' "$*"; }

[ -f "$VAULT/AGENTS.md" ] || { echo "ERROR: $VAULT/AGENTS.md not found — is the vault path right?" >&2; exit 1; }

# Print a file with the literal text $VAULT replaced by the real path.
# Pure bash on purpose: no delimiter to break on odd characters in the path.
render() { local c; c="$(cat "$1")"; printf '%s\n' "${c//\$VAULT/$VAULT}"; }

# Stamp the real vault path into SKILL.md's marked line (the rest of the skill refers to it).
stamp_skill() {
  local f="$SCRIPT_DIR/SKILL.md" line out=""
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      '**Vault path:**'*) line="**Vault path:** \`$VAULT\`" ;;
    esac
    out+="$line"$'\n'
  done < "$f"
  printf '%s' "$out" > "$f"
}

# Link (or copy) the skill folder into a tool's skills directory.
link_skill() {
  local dir="$1" target="$1/second-brain"
  mkdir -p "$dir"
  if [ -e "$target" ] && [ ! -L "$target" ]; then   # a real folder from an older install: keep it aside
    mv "$target" "$target.bak.$(date +%Y%m%d%H%M%S)"
    note "moved existing $target aside (.bak)"
  fi
  if ln -sfn "$SCRIPT_DIR" "$target" 2>/dev/null; then
    note "linked skill -> $target"
  else
    cp -R "$SCRIPT_DIR" "$target"; note "copied skill -> $target"
  fi
}

# Upsert the pointer block into a global instructions file (create, replace, or append).
upsert_block() {
  local target="$1" rendered
  mkdir -p "$(dirname "$target")"; touch "$target"
  rendered=$(mktemp); render "$SNIPPET" > "$rendered"
  if grep -qF "$BEGIN" "$target"; then
    awk -v b="$BEGIN" -v e="$END" -v f="$rendered" '
      $0==b {print; while ((getline line < f) > 0) if (line!=b && line!=e) print line; skip=1; next}
      $0==e {skip=0; print; next}
      skip!=1 {print}
    ' "$target" > "$target.tmp" && mv "$target.tmp" "$target"
    note "refreshed block in $target"
  else
    { printf '\n'; cat "$rendered"; } >> "$target"
    note "appended block to $target"
  fi
  rm -f "$rendered"
}

# No tool named: install for the known tools that already exist on this machine.
if [ $# -eq 0 ]; then
  [ -d "$HOME/.claude" ] && set -- "$@" claude
  [ -d "$HOME/.codex" ]  && set -- "$@" codex
  [ -d "$HOME/.gemini" ] && set -- "$@" gemini
  [ $# -gt 0 ] || { echo "No known agent tool found in $HOME. Name one: install.sh claude|codex|gemini" >&2; exit 1; }
fi

echo "Second-brain installer"
echo "  vault: $VAULT"
stamp_skill

for tool in "$@"; do
  case "$tool" in
    claude) echo "Claude:";     link_skill "$HOME/.claude/skills"; upsert_block "$HOME/.claude/CLAUDE.md" ;;
    codex)  echo "Codex:";      link_skill "$HOME/.codex/skills";  upsert_block "$HOME/.codex/AGENTS.md" ;;
    gemini) echo "Gemini CLI:"; upsert_block "$HOME/.gemini/GEMINI.md" ;;   # no skills folder: the pointer is the mechanism
    *) echo "Unknown tool '$tool' — install it by hand, see 'Other agents' in $SCRIPT_DIR/README.md" >&2 ;;
  esac
done

echo "Done. Restart your agent tool(s): the skill and the pointer are read when a session starts."
