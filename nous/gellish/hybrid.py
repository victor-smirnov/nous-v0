"""Hybrid documents: extract tables from a .md, inject tables back (spec/hybrid-format.md)."""
import pathlib, re

from .parse import FENCE, iter_blocks


def extract(doc, out_dir):
    """Write every ```gellish <id>``` block of doc as <out_dir>/<id>.txt (residual blocks as <id>.residual.txt)."""
    out_dir = pathlib.Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for kind, sid, lines in iter_blocks(doc):
        name = f"{sid}.txt" if kind == "gellish" else f"{sid}.residual.txt"
        (out_dir / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append(out_dir / name)
    return written


def inject(doc, tables, out=None):
    """Replace/append blocks in doc from table files. A table's section id is its file stem
    ('S2.2.txt' → S2.2; 'S2.2.residual.txt' → residual block). A block for a section that has
    no fence yet is appended under the heading named by a first line '# heading: <text>' if
    such a heading exists, else at the end of the document."""
    doc = pathlib.Path(doc)
    text = doc.read_text(encoding="utf-8") if doc.exists() else ""
    lines = text.splitlines()
    blocks = {}
    for t in tables:
        t = pathlib.Path(t)
        kind = "gellish-residual" if t.name.endswith(".residual.txt") else "gellish"
        sid = t.name[:-len(".residual.txt")] if kind == "gellish-residual" else t.stem
        body = [l for l in t.read_text(encoding="utf-8").splitlines()]
        heading = None
        if body and body[0].lower().startswith("# heading:"):
            heading = body[0].split(":", 1)[1].strip(); body = body[1:]
        while body and not body[-1].strip():
            body.pop()
        blocks[(kind, sid)] = (heading, body)

    # replace existing fences
    result, i, replaced = [], 0, set()
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m and (m.group(1), m.group(2)) in blocks:
            key = (m.group(1), m.group(2))
            result.append(lines[i]); result += blocks[key][1]
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                i += 1
            result.append("```"); replaced.add(key); i += 1
            continue
        result.append(lines[i]); i += 1

    # append the rest under their headings (or at the end)
    for key, (heading, body) in blocks.items():
        if key in replaced:
            continue
        fence = [f"```{key[0]} {key[1]}", *body, "```"]
        pos = None
        if heading:
            def is_heading(idx):
                return re.match(r"^#{1,6}\s+", result[idx]) is not None
            in_fence = False
            for j, l in enumerate(result):
                if l.startswith("```"):
                    in_fence = not in_fence; continue
                if not in_fence and is_heading(j) and l.lstrip("# ").strip().lower() == heading.lower():
                    pos = j + 1
                    inside = False
                    while pos < len(result):
                        if result[pos].startswith("```"):
                            inside = not inside
                        elif not inside and is_heading(pos):
                            break
                        pos += 1
                    break
        if pos is None:
            result += ["", *fence]
        else:
            result[pos:pos] = ["", *fence, ""]
    out = pathlib.Path(out) if out else doc
    out.write_text("\n".join(result).rstrip("\n") + "\n", encoding="utf-8")
    return out
