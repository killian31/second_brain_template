#!/usr/bin/env python3
"""Read-only vault health check for the `/second-brain lint` command.
Checks the frontmatter contract, wikilink integrity, orphans, INDEX drift,
and staleness/hygiene. Never writes anything — report first, fix what
the user names. Run: python3 00_Meta/scripts/lint.py

Scope: 00_Meta/** (Templates, skill, scripts, and the meta docs themselves)
and any Dashboards/** you add later (generated views, human-facing only) are
excluded from findings — tooling/infra, not vault notes. `_README.md` folder-doc files, the root
`README.md`, and `Daily/**` are exempt from the orphan check for the same
reason — daily notes are chronological records reached via LOG/INDEX, not
graph nodes expected to attract inbound links. All of the above still
count as valid link targets for notes that reference them.
"""
import os, re, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = ("/.obsidian/", "/.git/", "/00_Meta/", "/Dashboards/")
SKIP_FILES = {"INDEX.md", "LOG.md", "Inbox.md", "Home.md"}
ORPHAN_EXEMPT_PREFIXES = ("INDEX", "LOG", "Home", "Maps/", "Dashboards/",
                          "Daily/", "README.md")
# Daily notes are chronological records reached through LOG/INDEX, not graph
# nodes: their contract (Conventions §frontmatter) asks only for type/summary/
# created/tags, never `related`. Since LOG grants no inbound credit (below),
# every daily note would otherwise report as an orphan forever. README.md is
# repo documentation, not a note.
# Generated catalogs and append-only audit trails. They mention every note that
# exists or that ever changed, so a link *from* them is not evidence the target
# has a home in the graph — otherwise nothing would ever report as an orphan.
# Links in these files are still checked for breakage; they just grant no credit.
INBOUND_EXEMPT = {"INDEX.md", "LOG.md", "00_Meta/Consolidation Log.md"}
ALLOWED_TYPES = {"meta","moc","profile","experiment","project","person","topic",
                  "source","daily","org","idea","analysis","decision"}
ALLOWED_STATUS = {"idea","active","paused","done","abandoned"}
STATUS_TYPES = {"experiment","project","idea"}
today = datetime.date.today()

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

def strip_examples(body):
    """Remove fenced code, inline code, and HTML comments before scanning for
    wikilinks — these hold instructional example links (e.g. [[Note A]]) that
    aren't meant to resolve."""
    body = FENCE_RE.sub("", body)
    body = INLINE_CODE_RE.sub("", body)
    body = HTML_COMMENT_RE.sub("", body)
    return body

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    fm_text, body = m.group(1), m.group(2)
    fm = {"__fm_text__": fm_text}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        m2 = re.match(r"^(\w+):\s*(.*)$", lines[i])
        if m2:
            key, val = m2.group(1), m2.group(2).strip()
            if val == "" and i + 1 < len(lines) and lines[i + 1].strip().startswith("-"):
                items, j = [], i + 1
                while j < len(lines) and lines[j].strip().startswith("-"):
                    items.append(lines[j].strip()[1:].strip())
                    j += 1
                fm[key] = items
                i = j
                continue
            if key == "aliases" and val.startswith("[") and val.endswith("]"):
                fm[key] = [a.strip().strip('"').strip("'") for a in val[1:-1].split(",") if a.strip()]
            else:
                fm[key] = val
        i += 1
    return fm, body

# Walk the whole vault (any extension) so wikilinks/embeds to assets, Dashboards,
# and 00_Meta resolve — SKIP_DIRS only controls which files generate findings.
all_files, md_files = [], []
for p in glob.glob(os.path.join(ROOT, "**/*"), recursive=True):
    if not os.path.isfile(p):
        continue
    if any(d in p for d in ("/.obsidian/", "/.git/")):
        continue
    rel = p[len(ROOT) + 1:]
    all_files.append(rel)
    if rel.endswith(".md"):
        md_files.append(rel)
all_files.sort(); md_files.sort()

def is_skipped(rel):
    full = "/" + rel
    b = os.path.basename(rel)
    # README.md / _README.md are plain signposts (repo or folder), not vault
    # notes the frontmatter contract applies to — exempt entirely.
    return any(d in full for d in SKIP_DIRS) or b in SKIP_FILES or b == "README.md" or b.startswith("_README")

basenames = {}
for rel in all_files:
    basenames.setdefault(os.path.basename(rel), []).append(rel)
path_no_ext = {rel[:-3]: rel for rel in md_files}

notes = {}
for rel in md_files:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        text = f.read()
    fm, body = parse_frontmatter(text)
    notes[rel] = (fm, body)

def alias_resolve(target):
    """A link can also resolve via a target note's `aliases:` frontmatter.
    Returns the resolving note's path (so it can be credited an inbound link),
    or None if no alias matches."""
    target_l = target.split("|")[0].split("#")[0].strip().lower()
    for rel, (fm, _) in notes.items():
        if not fm:
            continue
        for a in fm.get("aliases", []) or []:
            if a.lower() == target_l or os.path.basename(a).lower() == target_l:
                return rel
    return None

high, medium, low = [], [], []
inbound = {rel: 0 for rel in md_files}

for rel, (fm, body) in notes.items():
    skipped = is_skipped(rel)
    clean_body = strip_examples(body)
    fm_text = (fm or {}).get("__fm_text__", "")
    links = WIKILINK_RE.findall(clean_body) + WIKILINK_RE.findall(fm_text)

    if not skipped:
        if fm is None:
            high.append(f"{rel}: missing YAML frontmatter entirely")
        else:
            typ = fm.get("type")
            if not typ:
                high.append(f"{rel}: missing `type`")
            elif typ not in ALLOWED_TYPES:
                high.append(f"{rel}: type `{typ}` outside allowed set")
            status = fm.get("status")
            if status and typ in STATUS_TYPES and status not in ALLOWED_STATUS:
                high.append(f"{rel}: status `{status}` invalid for type `{typ}`")
            summary = fm.get("summary", "")
            if not summary:
                high.append(f"{rel}: missing `summary`")
            else:
                wc = len(summary.split())
                norm_summary = summary.strip().lower().rstrip(".")
                norm_title = (fm.get("title", "") or "").strip().lower().strip('"')
                if wc < 8:
                    medium.append(f"{rel}: weak summary (<8 words): \"{summary}\"")
                elif norm_title and norm_summary == norm_title:
                    medium.append(f"{rel}: summary just restates the title")

            created, updated = fm.get("created"), fm.get("updated")
            if not updated:
                low.append(f"{rel}: missing `updated:`")
            elif created:
                try:
                    cd = datetime.date.fromisoformat(created[:10])
                    ud = datetime.date.fromisoformat(updated[:10])
                    if ud < cd:
                        low.append(f"{rel}: `updated:` ({updated}) earlier than `created:` ({created})")
                except ValueError:
                    pass
            if status == "active" and typ in ("experiment", "project") and updated:
                try:
                    ud = datetime.date.fromisoformat(updated[:10])
                    days = (today - ud).days
                    if days > 60:
                        low.append(f"{rel}: status active but `updated:` {updated} is {days}d old")
                except ValueError:
                    pass
            if typ == "topic":
                wc_body = len(re.sub(r"[#>*\-\[\]()`]", " ", clean_body).split())
                h2 = len(re.findall(r"^##\s", body, re.M))
                if wc_body > 400:
                    flag = f"{rel}: oversized topic note (~{wc_body} words)"
                    if h2 >= 2:
                        flag += f", {h2} ## sections -> split candidate"
                    low.append(flag)

    # Broken-link check + inbound-link counting run on every note (even skipped
    # ones) so a skipped note can still legitimately link elsewhere; but we only
    # *report* broken links for in-scope notes.
    broken = []
    credit_inbound = rel not in INBOUND_EXEMPT
    for link in links:
        norm = link.replace("\\|", "|")  # markdown-table-escaped alias pipe
        t = norm.split("|")[0].split("#")[0].strip()
        if not t:  # a bare [[#heading]] / [[|alias]] — nothing to resolve
            continue
        if t in path_no_ext:
            targets = [path_no_ext[t]]
        else:
            # Folder-less links ([[PEEK]] rather than [[Projects/PEEK]]) are the
            # common case, and Obsidian resolves them by basename. `basenames` is
            # keyed WITH the extension, so both spellings must be tried — missing
            # the `.md` form is what used to leave real links uncredited.
            b = os.path.basename(t)
            hits = basenames.get(b, []) + basenames.get(b + ".md", [])
            targets = [r2 for r2 in hits if r2.endswith(".md")]
            if not hits:
                # Not a file path; last chance is a target note's `aliases:`.
                alias_hit = alias_resolve(norm)
                if not alias_hit:
                    broken.append(t)
                    continue
                targets = [alias_hit]
        # `targets` is legitimately empty for embeds of non-note files
        # (![[chart.png]]) — those resolve, but there's no note to credit.
        if credit_inbound:
            for r2 in targets:
                inbound[r2] = inbound.get(r2, 0) + 1
    if broken and not skipped:
        medium.append(f"{rel}: broken wikilinks -> {', '.join(sorted(set(broken)))}")

for rel in md_files:
    if is_skipped(rel) or rel.startswith(ORPHAN_EXEMPT_PREFIXES) or rel == "Inbox.md":
        continue
    if os.path.basename(rel).startswith("_README"):  # folder-doc, not a retrieval note
        continue
    if inbound.get(rel, 0) == 0:
        medium.append(f"{rel}: orphan (zero inbound wikilinks)")

# INDEX.md drift
with open(os.path.join(ROOT, "INDEX.md"), encoding="utf-8") as f:
    index_text = f.read()
missing_from_index = []
for rel in md_files:
    if is_skipped(rel) or rel in SKIP_FILES or rel.startswith(("Dashboards/", "Maps/")):
        continue
    key, b = rel[:-3], os.path.basename(rel)[:-3]
    if key not in index_text and b not in index_text:
        missing_from_index.append(rel)
if missing_from_index:
    shown = ", ".join(missing_from_index[:20]) + (" ..." if len(missing_from_index) > 20 else "")
    medium.append(f"INDEX.md drift: {len(missing_from_index)} note(s) not found in INDEX.md -> {shown}")

# Inbox backlog
inbox_path = os.path.join(ROOT, "Inbox.md")
inbox_mtime = datetime.date.fromtimestamp(os.path.getmtime(inbox_path))
with open(inbox_path, encoding="utf-8") as f:
    bullets = [l for l in f.read().split("\n")
               if l.strip().startswith("- ") and "To process" not in l and l.strip() not in ("-", "- ")]
age = (today - inbox_mtime).days
if bullets:
    low.append(f"Inbox.md: {len(bullets)} bullet(s) pending, last modified {inbox_mtime} ({age}d ago)")

print(f"=== HIGH — contract violations: {len(high)} ===")
for x in high: print(" -", x)
print(f"\n=== MEDIUM — retrieval quality: {len(medium)} ===")
for x in medium: print(" -", x)
print(f"\n=== LOW — staleness & hygiene: {len(low)} ===")
for x in low: print(" -", x)
print(f"\n({len(md_files)} notes scanned, 00_Meta/ excluded from findings)")
