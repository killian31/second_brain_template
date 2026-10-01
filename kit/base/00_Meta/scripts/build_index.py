#!/usr/bin/env python3
"""Regenerate INDEX.md — a flat, greppable catalog of every note in the vault,
grouped by `type`, each with a one-line summary. Works for any agent reading
plain markdown, no plugins required. Run: python3 00_Meta/scripts/build_index.py

Summary source of truth: the `summary:` frontmatter field. If a note has no
`summary`, we fall back to its first plain body line (and the note should get a
real `summary` added — see 00_Meta/Conventions.md).
"""
import os, re, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = ("/.obsidian/", "/.git/", "/00_Meta/Templates/", "/00_Meta/skill/", "/00_Meta/scripts/")
SKIP_FILES = {"INDEX.md", "LOG.md", "Inbox.md"}
ORDER = ["project","decision","experiment","idea","analysis","topic","source","person","org","profile","daily","moc","meta"]

def parse(path):
    s = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", s, re.S)
    if not m: return None
    fm, body = m.group(1), m.group(2)
    def field(name):
        mm = re.search(rf"^{name}:\s*(.+)$", fm, re.M)
        return mm.group(1).strip().strip('"').strip("'") if mm else ""
    typ = field("type")
    if not typ or "{{" in fm: return None
    title = field("title") or os.path.splitext(os.path.basename(path))[0]
    updated = field("updated")
    # Prefer the explicit frontmatter summary; fall back to first plain body line.
    summary = field("summary")
    missing = not summary
    if not summary:
        for line in body.splitlines():
            t = line.strip()
            if not t: continue
            if t.startswith(("#",">","```","<!--","|","---","- [","* ")): continue
            t = re.sub(r"\[\[([^\]\|]+\|)?([^\]]+)\]\]", r"\2", t)   # wikilinks -> text
            t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)            # md links -> text
            t = re.sub(r"[*`_]", "", t)
            summary = t.strip()
            break
    # strip any residual wikilinks from a frontmatter summary too
    summary = re.sub(r"\[\[([^\]\|]+\|)?([^\]]+)\]\]", r"\2", summary)
    if len(summary) > 200: summary = summary[:197].rstrip() + "..."
    name = os.path.splitext(os.path.basename(path))[0]
    return {"type": typ, "title": title, "name": name, "updated": updated, "summary": summary, "missing": missing}

notes = []
for p in glob.glob(os.path.join(ROOT, "**/*.md"), recursive=True):
    rp = p[len(ROOT):]
    if any(d in p for d in SKIP_DIRS): continue
    if os.path.basename(p) in SKIP_FILES: continue
    n = parse(p)
    if n: notes.append(n)

by = {}
for n in notes: by.setdefault(n["type"], []).append(n)
today = datetime.date.today().isoformat()
missing = sum(1 for n in notes if n["missing"])

out = []
out.append("---")
out.append("type: meta")
out.append("title: INDEX")
out.append("aliases: [INDEX, Catalog]")
out.append(f"created: {today}")
out.append(f"updated: {today}")
out.append("tags: [meta/entrypoint]")
out.append('related: ["[[AGENTS]]", "[[LOG]]"]')
out.append("---")
out.append("")
out.append("# INDEX")
out.append("")
tail = f" {missing} note(s) still lack a `summary:` field." if missing else " Every note has a `summary`."
out.append(f"> Auto-generated flat catalog of every note ({len(notes)} total), grouped by `type`.{tail} **Do not hand-edit** — regenerate with `python3 00_Meta/scripts/build_index.py`. Last built: {today}.")
out.append("")
seen = set()
for typ in ORDER + sorted(k for k in by if k not in ORDER):
    if typ not in by: continue
    seen.add(typ)
    items = sorted(by[typ], key=lambda n: n["name"].lower())
    out.append(f"## {typ} ({len(items)})")
    for n in items:
        s = f" — {n['summary']}" if n["summary"] else ""
        out.append(f"- [[{n['name']}]]{s}")
    out.append("")

open(os.path.join(ROOT, "INDEX.md"), "w", encoding="utf-8").write("\n".join(out))
print(f"INDEX.md written: {len(notes)} notes across {len(by)} types; {missing} missing summary")
