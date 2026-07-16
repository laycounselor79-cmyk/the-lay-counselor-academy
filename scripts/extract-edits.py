#!/usr/bin/env python3
"""Extract Elizabeth's suggested edits and comments from a downloaded
Google Docs .docx file with Suggesting-mode track changes preserved.

Outputs a clean side-by-side report grouped by document section so we can
review what's actually being changed before applying anything to the site.
"""
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX = Path("/Users/scottpope/Downloads/LCA — Site Copy for Review.docx")
OUT = Path(__file__).resolve().parent.parent / "ELIZABETHS_EDITS.md"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def parse_xml(zipf, name):
    with zipf.open(name) as f:
        return ET.parse(f).getroot()


def text_of(node):
    """Concatenate all <w:t> text inside a node."""
    return "".join(t.text or "" for t in node.iter(f"{W}t"))


def load_comments(zipf):
    """Return dict id -> {author, text}."""
    try:
        root = parse_xml(zipf, "word/comments.xml")
    except KeyError:
        return {}
    out = {}
    for c in root.findall(f"{W}comment"):
        cid = c.get(f"{W}id")
        author = c.get(f"{W}author", "?")
        body = " ".join(text_of(p) for p in c.findall(f"{W}p"))
        out[cid] = {"author": author, "text": body.strip()}
    return out


def extract_walk(doc_root, comments):
    """Walk the body in document order, emit:
      (kind, payload)
    where kind ∈ {"label", "para", "ins", "del", "comment"}.

    "label" is a bracketed anchor like [HOME / HERO / HEADLINE] — we treat
    them as section breadcrumbs so the output is grouped by site element.
    """
    body = doc_root.find(f"{W}body")
    if body is None:
        return []

    events = []
    label_re = re.compile(r"^\s*\[[A-Z0-9][^\]]*\]\s*$")

    open_comments = {}

    def walk(node, in_ins=False, in_del=False):
        tag = node.tag
        # Insertions / deletions wrap their runs; recurse with flag set
        if tag == f"{W}ins":
            for child in node:
                walk(child, in_ins=True, in_del=in_del)
            return
        if tag == f"{W}del":
            for child in node:
                walk(child, in_ins=in_ins, in_del=True)
            return
        if tag == f"{W}commentRangeStart":
            cid = node.get(f"{W}id")
            open_comments[cid] = []
            return
        if tag == f"{W}commentRangeEnd":
            cid = node.get(f"{W}id")
            anchored = "".join(open_comments.pop(cid, []))
            events.append(("comment", {"id": cid, "anchored": anchored.strip()}))
            return
        if tag == f"{W}r":
            # a run — collect its text
            txt = ""
            for t in node.iter(f"{W}t"):
                txt += t.text or ""
            # Word stores deleted text in <w:delText> under deletion runs
            for t in node.iter(f"{W}delText"):
                txt += t.text or ""
            if not txt:
                return
            if in_ins:
                events.append(("ins", txt))
            elif in_del:
                events.append(("del", txt))
            else:
                events.append(("text", txt))
            # also track text inside open comment ranges
            for cid in open_comments:
                open_comments[cid].append(txt)
            return
        # generic descent
        for child in node:
            walk(child, in_ins=in_ins, in_del=in_del)

    # Emit a paragraph break between top-level <w:p> blocks
    for p in body.findall(f"{W}p"):
        walk(p)
        events.append(("para", None))

    return events


def collapse_paragraphs(events):
    """Group consecutive non-para events into paragraphs.

    Returns a list of paragraphs, each is a list of (kind, text) tuples
    where kind ∈ {"text", "ins", "del", "comment"}.
    """
    paragraphs = []
    current = []
    for kind, payload in events:
        if kind == "para":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append((kind, payload))
    if current:
        paragraphs.append(current)
    return paragraphs


def paragraph_to_strings(para):
    """Return (original_text, suggested_text, has_changes, comments_here).

    original = base text + deletions, ignoring insertions
    suggested = base text + insertions, ignoring deletions
    """
    orig_parts = []
    sug_parts = []
    has_changes = False
    comments_here = []
    for kind, payload in para:
        if kind == "text":
            orig_parts.append(payload)
            sug_parts.append(payload)
        elif kind == "ins":
            sug_parts.append(payload)
            has_changes = True
        elif kind == "del":
            orig_parts.append(payload)
            has_changes = True
        elif kind == "comment":
            comments_here.append(payload)
    return ("".join(orig_parts), "".join(sug_parts), has_changes, comments_here)


def main():
    if not DOCX.exists():
        print(f"NOT FOUND: {DOCX}", file=sys.stderr)
        sys.exit(1)

    with zipfile.ZipFile(DOCX) as zf:
        doc = parse_xml(zf, "word/document.xml")
        comments = load_comments(zf)

    events = extract_walk(doc, comments)
    paragraphs = collapse_paragraphs(events)

    lines = []
    lines.append("# Elizabeth's Edits — extracted from the downloaded .docx\n")
    lines.append(f"Source: `{DOCX}`\n")
    lines.append(f"Total comments: **{len(comments)}**\n")

    # Summary counts
    total_ins = total_del = 0
    for para in paragraphs:
        for kind, _ in para:
            if kind == "ins":
                total_ins += 1
            elif kind == "del":
                total_del += 1
    lines.append(f"Total suggested insertions: **{total_ins}** · deletions: **{total_del}**\n")
    lines.append("---\n")

    # Walk paragraphs. Use bracket-label paragraphs as section anchors.
    label_re = re.compile(r"^\s*\[[A-Z0-9][^\]]*\]\s*$")
    pending_label = None
    edit_n = 0
    for para in paragraphs:
        orig, sug, has_changes, comments_here = paragraph_to_strings(para)
        # Use the plain (no-change) version to detect labels
        plain = orig if orig else sug
        plain_stripped = plain.strip()
        if not plain_stripped:
            continue
        if label_re.match(plain_stripped):
            pending_label = plain_stripped
            continue
        if has_changes or comments_here:
            edit_n += 1
            lines.append(f"## Edit {edit_n}")
            if pending_label:
                lines.append(f"**Label:** `{pending_label}`\n")
            lines.append(f"**Original:**\n\n> {orig.strip() or '_(empty)_'}\n")
            lines.append(f"**Suggested:**\n\n> {sug.strip() or '_(empty)_'}\n")
            for c in comments_here:
                cid = c["id"]
                meta = comments.get(cid, {})
                author = meta.get("author", "?")
                body = meta.get("text", "")
                anchored = c["anchored"]
                lines.append(
                    f"**Comment** _(by {author}, anchored to_ "
                    f"`{anchored[:80]}{'…' if len(anchored) > 80 else ''}`_)_:\n\n> {body}\n"
                )
            lines.append("")
            pending_label = None  # consume the label

    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"  {edit_n} paragraphs with edits or comments")
    print(f"  {total_ins} insertions, {total_del} deletions, {len(comments)} comments")


if __name__ == "__main__":
    main()
