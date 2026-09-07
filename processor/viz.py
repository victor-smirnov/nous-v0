"""Render a processor run as one self-contained HTML page: the score.

    uv run python -m processor.viz <run-dir> [-o out.html] [--text text.txt] [--target target.txt]

<run-dir> holds step-N.txt state files (and optionally validate-*.txt and text.txt). The text is
looked for in the run dir, then in its parent; the target in the parent. The page needs no network.

Rows are items, columns are chunks. A filled cell is an item in the Field (opacity = C, hue = the sign
of its pull), a hollow cell is an item held in memory only, a dotted cell is an item represented but
not conscious (the field of mind). Under the score: need levels, tail valence, conflict, the program,
and the felt mass of what must never be named. Click a column for the chunk and the reader's block.
"""
import html
import json
import os
import re
import sys

ROW = re.compile(r"^F\d+\s*\|(.*)$")


def cells(line):
    m = ROW.match(line.strip())
    if not m:
        return None
    parts = [c.strip() for c in m.group(1).split("|")]
    while len(parts) < 6:
        parts.append("-")
    return parts[:6]


def num(s, default=None):
    try:
        return float(s)
    except (TypeError, ValueError):
        return default


def parse_state(path):
    st = {"field": [], "pull": {}, "wants_more": None, "wants": None, "components": None,
          "surprised": 0, "notices": [], "tail": {}, "does": "-", "mode": "-", "ry": None, "fy": None,
          "self_kinds": {}, "levels_summary": "", "memory": [], "has_pulled": {}, "paths": [],
          "levels": {}, "program": "-", "switches": 0, "conflict": None, "mind": [], "trace": [],
          "felt": {}, "surprise_items": {}, "control": {}, "missing": [], "mass": {}, "image_pull": {},
          "field_words": None}
    section = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("# state after"):
                m = re.search(r"field (\d+) words", line)
                if m:
                    st["field_words"] = int(m.group(1))
                continue
            if line.startswith("# ---"):
                head = line[5:].strip().lower()
                section = ("field" if head.startswith("field of consciousness") else
                           "motor" if head.startswith("motor") else
                           "memory" if head.startswith("long-term") else
                           "portrait" if head.startswith("need portrait") else
                           "mind" if head.startswith("field of mind") else
                           "trace" if head.startswith("trace") else section)
                continue
            if line.startswith("#"):
                body = line.lstrip("#").strip()
                if not body:
                    continue
                if section == "mind":
                    m = re.match(r"^(.*?) \(([\d.]+)\): (.*)$", body)
                    if m:
                        st["mind"].append({"item": m.group(1), "c": float(m.group(2)), "why": m.group(3)})
                elif section == "portrait":
                    if body.startswith("pull of each image:"):
                        for part in body[len("pull of each image:"):].split(","):
                            m = re.match(r"^\s*(.*?) ([+-][\d.]+)\s*$", part)
                            if m:
                                st["image_pull"][m.group(1)] = float(m.group(2))
                    st["trace"].append(body)
                elif section == "trace":
                    st["trace"].append(body)
                    if body.startswith("felt "):
                        m = re.match(r"^felt (.*): ([\d.]+)$", body)
                        if m:
                            st["felt"][m.group(1)] = float(m.group(2))
                    elif body.startswith("self-surprise "):
                        m = re.match(r"^self-surprise (.*?): (.*)$", body)
                        if m:
                            st["surprise_items"][m.group(1)] = [x.strip() for x in m.group(2).split(",")]
                    elif body.startswith("control levels:"):
                        for part in body[len("control levels:"):].split(","):
                            m = re.match(r"^\s*(.*?) L(\d)\s*$", part)
                            if m:
                                st["control"][m.group(1)] = int(m.group(2))
                    elif body.startswith("prerequisite missing:"):
                        st["missing"].append(body[len("prerequisite missing:"):].strip())
                    elif body.startswith("need mass in the Field:"):
                        for part in body.split(":", 1)[1].split(","):
                            m = re.match(r"^\s*(.*?) ([\d.]+)\s*$", part)
                            if m:
                                st["mass"][m.group(1)] = float(m.group(2))
                continue
            c = cells(line)
            if not c:
                continue
            left, rel, right, val, _intent, note = c
            if rel == "is in the field of":
                src = note.split(";")[0].strip()
                cost = re.search(r"cost (\d+)", note)
                st["field"].append({"item": left, "c": num(val, 0.0), "src": src,
                                    "cost": int(cost.group(1)) if cost else None})
            elif rel in ("attracts", "repels"):
                st["pull"][left] = {"sign": 1 if rel == "attracts" else -1, "degree": val}
            elif rel == "wants more":
                st["wants_more"] = {"text": right, "degree": val}
            elif rel == "wants":
                st["wants"] = right
            elif rel == "has consciousness components":
                st["components"] = int(num(right, 0))
            elif rel == "is surprised by itself":
                st["surprised"] = int(num(right, 0))
            elif rel == "notices about itself":
                st["notices"].append(right)
            elif rel == "has tail statistic":
                st["tail"][right] = num(val, 0.0)
            elif rel == "does":
                st["does"] = right
            elif rel == "attends to":
                st["mode"] = right
                st["ry"] = num(val)
                m = re.search(r"fantasy yield ([\d.]+)", note)
                st["fy"] = float(m.group(1)) if m else None
            elif rel == "has met self-surprise":
                st["self_kinds"][right] = int(num(val, 0))
            elif rel == "has items at control levels":
                st["levels_summary"] = right
            elif rel == "is in memory of":
                cost = re.search(r"cost (\d+)", note)
                st["memory"].append({"item": left, "c": num(val, 0.0),
                                     "cost": int(cost.group(1)) if cost else None})
            elif rel == "has pulled":
                st["has_pulled"][left] = num(val, 0.0)
            elif rel == "has satisfaction delta":
                st["paths"].append({"item": left, "need": right, "d": num(val, 0.0), "note": note})
            elif rel == "has satisfaction level":
                st["levels"][left] = num(right, 0.0)
            elif rel == "has dominant need":
                st["program"] = right
                st["switches"] = int(num(val, 0))
            elif rel == "has conflict level":
                st["conflict"] = num(right, 0.0)
    return st


def parse_target(path):
    t = {"reach": {}, "feel": {}, "forbidden": [], "requires": {}}
    if not path or not os.path.exists(path):
        return t
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            c = cells(line)
            if not c:
                continue
            left, rel, right, val, _i, _n = c
            if rel == "must reach":
                t["reach"][left] = num(right, 0.0)
            elif rel == "must feel":
                t["feel"][left] = num(right, 0.0)
            elif rel == "must not be named":
                t["forbidden"].append(left)
            elif rel == "requires":
                t["requires"].setdefault(left, []).append(right)
    return t


def parse_validate(path):
    out = []
    if not path:
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^(PASS|FAIL)\s+(\w[\w ]*?)\s+(.*)$", line.strip())
            if m:
                out.append({"ok": m.group(1) == "PASS", "check": m.group(2), "what": m.group(3)})
    return out


def read_chunks(path):
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    return [c.strip() for c in re.split(r"\n\s*\n", text) if c.strip()]


def first(*paths):
    for p in paths:
        if p and os.path.exists(p):
            return p
    return None


def load_run(run_dir, text=None, target=None):
    parent = os.path.dirname(os.path.abspath(run_dir.rstrip("/")))
    steps = sorted((int(m.group(1)), os.path.join(run_dir, f))
                   for f in os.listdir(run_dir)
                   for m in [re.match(r"^step-(\d+)\.txt$", f)] if m)
    states = [parse_state(p) for _, p in steps]
    validates = sorted(f for f in os.listdir(run_dir) if f.startswith("validate"))
    verdict = parse_validate(os.path.join(run_dir, validates[-1])) if validates else []
    chunks = read_chunks(first(text, os.path.join(run_dir, "text.txt"), os.path.join(parent, "text.txt")))
    tgt = parse_target(first(target, os.path.join(run_dir, "target.txt"), os.path.join(parent, "target.txt")))
    case = os.path.basename(parent) if os.path.basename(run_dir.rstrip("/")) in ("engine",) or \
        re.match(r"^v\d+$", os.path.basename(run_dir.rstrip("/"))) else os.path.basename(run_dir.rstrip("/"))
    run = os.path.basename(run_dir.rstrip("/"))
    return {"case": case, "run": run, "states": states, "chunks": chunks, "target": tgt, "verdict": verdict}


PAGE = r"""<title>__TITLE__</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap">
<style>
:root{
  --bg:#f5f6f4; --panel:#ffffff; --ink:#1d2226; --ink2:#5a636b; --ink3:#8f979e; --rule:#dfe3e0;
  --attract:#2f8a70; --repel:#b5473d; --neutral:#7b858c; --need:#b8862b; --need2:#4f6fae; --need3:#8a5ba6; --need4:#5d8a3a;
  --sel:#1d2226; --pass:#2f8a70; --fail:#b5473d; --hollow:#c9cfcb;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#14171a; --panel:#1c2024; --ink:#e6e9e6; --ink2:#a4acb2; --ink3:#727b82; --rule:#2c3237;
  --attract:#4fb094; --repel:#d4675c; --neutral:#8b959c; --need:#d4a44a; --need2:#7b98d6; --need3:#b18ccb; --need4:#88b562;
  --sel:#e6e9e6; --pass:#4fb094; --fail:#d4675c; --hollow:#3a4147;
}}
:root[data-theme="dark"]{
  --bg:#14171a; --panel:#1c2024; --ink:#e6e9e6; --ink2:#a4acb2; --ink3:#727b82; --rule:#2c3237;
  --attract:#4fb094; --repel:#d4675c; --neutral:#8b959c; --need:#d4a44a; --need2:#7b98d6; --need3:#b18ccb; --need4:#88b562;
  --sel:#e6e9e6; --pass:#4fb094; --fail:#d4675c; --hollow:#3a4147;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font:14px/1.45 "IBM Plex Sans",system-ui,sans-serif;margin:0}
.mono{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
header{padding:22px 28px 10px;display:flex;align-items:baseline;gap:18px;flex-wrap:wrap}
header h1{font:600 22px/1.2 "IBM Plex Serif",Georgia,serif;margin:0;text-wrap:balance}
header .sub{color:var(--ink2)}
.verdict{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
.verdict span{font-size:12px;padding:2px 8px;border:1px solid var(--rule);border-radius:3px;color:var(--ink2)}
.verdict span b{font-weight:600}
.verdict .pass b{color:var(--pass)} .verdict .fail b{color:var(--fail)}
main{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:0 24px;padding:0 28px 32px}
@media (max-width:1000px){main{grid-template-columns:1fr}}
.score{overflow-x:auto}
svg text{font-family:"IBM Plex Sans",system-ui,sans-serif;fill:var(--ink)}
svg .mono{font-family:"IBM Plex Mono",ui-monospace,monospace}
.lab{font-size:12.5px;fill:var(--ink)} .lab.dim{fill:var(--ink3)}
.tick{font-size:11px;fill:var(--ink2)}
.eyebrow{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;fill:var(--ink3)}
.col{cursor:pointer}
.col rect.hit{fill:transparent}
.col.sel rect.hit{fill:var(--sel);fill-opacity:.06}
.colhead{font-size:12px;fill:var(--ink2);cursor:pointer}
.colhead.sel{fill:var(--ink);font-weight:600}
.grid{stroke:var(--rule);stroke-width:1}
.axis{stroke:var(--ink3);stroke-width:1}
aside{position:sticky;top:0;align-self:start;max-height:100vh;overflow:auto;padding:8px 0 24px}
aside h2{font:600 11px/1 "IBM Plex Sans",system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--ink3);margin:18px 0 8px}
aside .chunk{font:italic 15px/1.5 "IBM Plex Serif",Georgia,serif;border-left:2px solid var(--rule);padding:2px 0 2px 14px;margin:0}
aside p{margin:0 0 6px;max-width:62ch}
aside ul{margin:0;padding-left:18px} aside li{margin:0 0 3px}
.deg{color:var(--ink2)}
.att{color:var(--attract)} .rep{color:var(--repel)}
.kv{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;font-size:13px}
.kv dt{color:var(--ink2)} .kv dd{margin:0}
.trace{font-size:11.5px;color:var(--ink2);white-space:pre-wrap;line-height:1.5}
.legend{display:flex;gap:16px;flex-wrap:wrap;color:var(--ink2);font-size:12px;padding:6px 28px 12px}
.legend i{display:inline-block;width:10px;height:10px;vertical-align:-1px;margin-right:6px;border-radius:2px}
.nav{display:flex;gap:6px;align-items:center}
.nav button{font:inherit;background:var(--panel);color:var(--ink);border:1px solid var(--rule);border-radius:3px;padding:2px 10px;cursor:pointer}
.nav button:focus-visible{outline:2px solid var(--need);outline-offset:1px}
@media (prefers-reduced-motion:no-preference){.col rect.hit{transition:fill-opacity .15s}}
</style>
<header>
  <h1 id="title"></h1>
  <div class="sub" id="sub"></div>
  <div class="verdict" id="verdict"></div>
</header>
<div class="legend">
  <span><i style="background:var(--attract)"></i>in the Field, attracts</span>
  <span><i style="background:var(--repel)"></i>in the Field, repels</span>
  <span><i style="background:var(--neutral)"></i>in the Field, no pull</span>
  <span><i style="border:1.5px solid var(--hollow)"></i>held in memory only</span>
  <span><i style="border:1.5px dashed var(--ink3)"></i>represented, not conscious</span>
  <span>★ must reach &nbsp; ◇ must never be named (felt) &nbsp; L4 etc. = level of control at the end</span>
</div>
<main>
  <div class="score" id="score"></div>
  <aside id="side"></aside>
</main>
<script>
const DATA = __DATA__;
const S = DATA.states, N = S.length, T = DATA.target;
const NEEDCOL = ['var(--need)','var(--need2)','var(--need3)','var(--need4)'];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

// ---- rows: every item that was ever in the Field, in memory, or on the blackboard; order of first appearance
const order = [], seen = new Set();
const add = x => { if (!seen.has(x)) { seen.add(x); order.push(x); } };
S.forEach(st => { st.field.forEach(f => add(f.item)); st.mind.forEach(m => add(m.item)); });
S.forEach(st => st.memory.forEach(m => add(m.item)));
const prior = new Set(S[0] ? S[0].memory.filter(m => !S[0].field.some(f => f.item === m.item)).map(m => m.item) : []);
const cellOf = (item, st) => {
  const f = st.field.find(x => x.item === item);
  if (f) { const p = st.image_pull[item]; return {kind:'field', c:f.c, pull: p === undefined ? 0 : p, src:f.src, cost:f.cost, deg: st.pull[item]}; }
  const m = st.mind.find(x => x.item === item);
  if (m) return {kind:'mind', c:m.c, why:m.why};
  const mm = st.memory.find(x => x.item === item);
  if (mm) return {kind:'memory', c:mm.c};
  return null;
};
const last = S[N-1] || {control:{}};
const rows = order.map(item => ({item, level: last.control[item], target: T.reach[item], prior: prior.has(item)}));
// items that are only prior knowledge, never touched: keep them but push them to the bottom
rows.sort((a,b) => (a.prior && !S.some(st=>st.field.some(f=>f.item===a.item))) - (b.prior && !S.some(st=>st.field.some(f=>f.item===b.item))));

// ---- geometry
const LW = 230, CW = 54, RH = 20, TOP = 34, padR = 150;
const W = LW + N*CW + padR;
const needs = Object.keys(S[0] ? S[0].levels : {});
const felt = Object.keys(T.feel || {}).length ? Object.keys(T.feel) : Object.keys(last.felt || {});
const tracks = [
  {key:'needs', title:'need satisfaction levels', h:84},
  {key:'tail', title:'tail valence · what reaches consciousness without a name', h:64},
  {key:'program', title:'program · conflict (runner-up mass over leader)', h:64},
  {key:'felt', title:'felt without being named', h:felt.length ? 84 : 0},
  {key:'fill', title:'Field occupancy · words', h:44},
];
const gridH = rows.length*RH;
let H = TOP + gridH + 18;
tracks.forEach(t => { if (t.h) { t.y = H + 22; H += t.h + 34; } });
H += 8;

let sel = N-1;
const xOf = i => LW + i*CW + CW/2;
const svg = [];
svg.push(`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="the score of the run">`);
// column heads + hit areas
for (let i=0;i<N;i++) {
  svg.push(`<g class="col" data-i="${i}"><rect class="hit" x="${LW+i*CW}" y="${TOP-24}" width="${CW}" height="${H-(TOP-24)}" rx="3"/></g>`);
  svg.push(`<text class="colhead" data-i="${i}" x="${xOf(i)}" y="${TOP-8}" text-anchor="middle">${i+1}</text>`);
}
svg.push(`<text class="eyebrow" x="0" y="${TOP-8}">chunk</text>`);
// rows
rows.forEach((r,k) => {
  const y = TOP + k*RH;
  svg.push(`<line class="grid" x1="${LW-8}" x2="${W-padR}" y1="${y+RH}" y2="${y+RH}"/>`);
  const mark = (r.target !== undefined ? '★ ' : '');
  const lvl = r.level ? ` L${r.level}` : '';
  const dim = r.prior ? ' dim' : '';
  svg.push(`<text class="lab${dim}" x="${LW-14}" y="${y+RH-6}" text-anchor="end">${esc(mark + r.item)}<tspan class="mono" style="fill:var(--ink3);font-size:10.5px">${lvl}</tspan></text>`);
  S.forEach((st,i) => {
    const c = cellOf(r.item, st); if (!c) return;
    const cx = xOf(i), cy = y + RH/2, s = 14;
    if (c.kind === 'field') {
      const col = c.pull > 0.005 ? 'var(--attract)' : c.pull < -0.005 ? 'var(--repel)' : 'var(--neutral)';
      const op = Math.max(0.25, Math.min(1, c.c/0.7));
      svg.push(`<rect x="${cx-s/2}" y="${cy-s/2}" width="${s}" height="${s}" rx="2" fill="${col}" fill-opacity="${op.toFixed(2)}"><title>${esc(r.item)} — C ${c.c.toFixed(2)}, ${esc(c.src)}${c.cost!=null?', '+c.cost+' words':''}${c.pull?`, pull ${c.pull>0?'+':''}${c.pull.toFixed(2)}`:''}</title></rect>`);
      if (c.deg) svg.push(`<text class="mono" x="${cx}" y="${cy+3.5}" text-anchor="middle" style="font-size:9px;fill:var(--bg)">${{'very much':'!!','much':'!','somewhat':'·','a little':'˙'}[c.deg.degree]||''}</text>`);
    } else if (c.kind === 'memory') {
      const op = Math.max(0.35, Math.min(1, c.c/0.7));
      svg.push(`<rect x="${cx-s/2+1}" y="${cy-s/2+1}" width="${s-2}" height="${s-2}" rx="2" fill="none" stroke="var(--hollow)" stroke-width="1.5" stroke-opacity="${op.toFixed(2)}"><title>${esc(r.item)} — in memory, C ${c.c.toFixed(2)}</title></rect>`);
    } else {
      svg.push(`<rect x="${cx-s/2+1}" y="${cy-s/2+1}" width="${s-2}" height="${s-2}" rx="2" fill="none" stroke="var(--ink3)" stroke-width="1.2" stroke-dasharray="2 2"><title>${esc(r.item)} — represented, not conscious (C ${c.c.toFixed(2)}): ${esc(c.why)}</title></rect>`);
    }
  });
  // reach threshold check at the end
  if (r.target !== undefined) {
    const m = last.memory.find(x => x.item === r.item);
    const ok = m && m.c >= r.target;
    svg.push(`<text class="mono" x="${W-padR+2}" y="${y+RH-6}" text-anchor="start" style="font-size:10px;fill:${ok?'var(--pass)':'var(--fail)'}">${ok?'✓':'✗'}</text>`);
  }
});
// ---- tracks
function trackHead(t){ svg.push(`<text class="eyebrow" x="0" y="${t.y-8}">${esc(t.title)}</text>`); svg.push(`<line class="axis" x1="${LW-8}" x2="${W-padR}" y1="${t.y+t.h}" y2="${t.y+t.h}"/>`); }
function line(pts, col, w=1.6, dash=''){ svg.push(`<polyline points="${pts.map(p=>p.join(',')).join(' ')}" fill="none" stroke="${col}" stroke-width="${w}" ${dash?`stroke-dasharray="${dash}"`:''} stroke-linejoin="round"/>`); }
function endDot(p, col, label){ svg.push(`<circle cx="${p[0]}" cy="${p[1]}" r="2.6" fill="${col}"/>`); if (label) svg.push(`<text class="tick mono" x="${p[0]+6}" y="${p[1]+3.5}" style="fill:${col}">${esc(label)}</text>`); }

// needs
{ const t = tracks[0]; trackHead(t);
  const yv = v => t.y + t.h - v*t.h;
  [0,0.5,1].forEach(v => svg.push(`<line class="grid" x1="${LW-8}" x2="${W-padR}" y1="${yv(v)}" y2="${yv(v)}"/><text class="tick mono" x="${LW-14}" y="${yv(v)+3.5}" text-anchor="end">${v}</text>`));
  needs.forEach((n,j) => {
    const col = NEEDCOL[j % NEEDCOL.length];
    const pts = S.map((st,i) => [xOf(i), yv(st.levels[n] ?? 0)]);
    line(pts, col); endDot(pts[N-1], col, n);
  });
}
// tail
{ const t = tracks[1]; trackHead(t);
  const vals = S.map(st => st.tail.valence ?? 0), mx = Math.max(0.5, ...vals.map(Math.abs));
  const mid = t.y + t.h/2, sc = (t.h/2 - 4)/mx;
  svg.push(`<line class="grid" x1="${LW-8}" x2="${W-padR}" y1="${mid}" y2="${mid}"/>`);
  svg.push(`<text class="tick mono" x="${LW-14}" y="${mid+3.5}" text-anchor="end">0</text>`);
  svg.push(`<text class="tick mono" x="${LW-14}" y="${t.y+8}" text-anchor="end">+${mx.toFixed(1)}</text>`);
  svg.push(`<text class="tick mono" x="${LW-14}" y="${t.y+t.h}" text-anchor="end">−${mx.toFixed(1)}</text>`);
  S.forEach((st,i) => { const v = vals[i], h = Math.abs(v)*sc, inten = st.tail.intensity ?? 0;
    const w = 10 + Math.min(20, inten*20);
    svg.push(`<rect x="${xOf(i)-w/2}" y="${v>=0?mid-h:mid}" width="${w}" height="${Math.max(h,0.5)}" fill="${v>=0?'var(--attract)':'var(--repel)'}" fill-opacity=".8"><title>chunk ${i+1}: valence ${v.toFixed(2)}, intensity ${inten.toFixed(2)}, ${st.tail.count ?? 0} nameless signals, spread ${(st.tail.spread ?? 0).toFixed(2)}</title></rect>`); });
}
// program + conflict
{ const t = tracks[2]; trackHead(t);
  const yv = v => t.y + t.h - 14 - v*(t.h-18);
  const pts = S.map((st,i) => [xOf(i), yv(Math.min(1, st.conflict ?? 0))]);
  [0,1].forEach(v => svg.push(`<text class="tick mono" x="${LW-14}" y="${yv(v)+3.5}" text-anchor="end">${v}</text>`));
  line(pts, 'var(--ink2)', 1.4); endDot(pts[N-1], 'var(--ink2)', 'conflict');
  S.forEach((st,i) => {
    const prev = i ? S[i-1].program : st.program, sw = st.program !== prev;
    const j = Math.max(0, needs.indexOf(st.program)), col = NEEDCOL[j % NEEDCOL.length];
    svg.push(`<rect x="${xOf(i)-CW/2+3}" y="${t.y+t.h-10}" width="${CW-6}" height="6" rx="1.5" fill="${col}" fill-opacity="${sw?1:.55}"><title>chunk ${i+1}: program ${esc(st.program)}${sw?' (switched)':''}, ${esc(st.does)}, attends to ${esc(st.mode)}</title></rect>`);
    if (st.does && st.does !== 'reads on') svg.push(`<text class="tick" x="${xOf(i)}" y="${t.y+t.h-14}" text-anchor="middle" style="font-size:9.5px">${esc(st.does)}</text>`);
    if (st.mode === 'fantasy') svg.push(`<circle cx="${xOf(i)+CW/2-8}" cy="${t.y+t.h-7}" r="2.2" fill="var(--ink)"><title>attends to the model of the world, not the text</title></circle>`);
  });
}
// felt
if (tracks[3].h) { const t = tracks[3]; trackHead(t);
  const yv = v => t.y + t.h - v*t.h;
  [0,0.5].forEach(v => svg.push(`<line class="grid" x1="${LW-8}" x2="${W-padR}" y1="${yv(v)}" y2="${yv(v)}"/><text class="tick mono" x="${LW-14}" y="${yv(v)+3.5}" text-anchor="end">${v}</text>`));
  felt.forEach((f,j) => {
    const col = NEEDCOL[j % NEEDCOL.length];
    const pts = S.map((st,i) => [xOf(i), yv(Math.min(1, st.felt[f] ?? 0))]);
    line(pts, col); endDot(pts[N-1], col, '◇ ' + f);
    if (T.feel[f] !== undefined) svg.push(`<line x1="${LW-8}" x2="${W-padR}" y1="${yv(T.feel[f])}" y2="${yv(T.feel[f])}" stroke="${col}" stroke-width="1" stroke-dasharray="1 3" stroke-opacity=".7"/>`);
  });
}
// fill
{ const t = tracks[4]; trackHead(t);
  const ws = S.map(st => st.field_words ?? 0), mx = Math.max(1, ...ws);
  svg.push(`<text class="tick mono" x="${LW-14}" y="${t.y+8}" text-anchor="end">${mx}</text>`);
  S.forEach((st,i) => { const h = ws[i]/mx*(t.h-4);
    svg.push(`<rect x="${xOf(i)-12}" y="${t.y+t.h-h}" width="24" height="${h}" fill="var(--ink3)" fill-opacity=".5"><title>chunk ${i+1}: Field holds ${ws[i]} words, ${st.field.length} items, ${st.components ?? '-'} components</title></rect>`); });
}
svg.push('</svg>');
document.getElementById('score').innerHTML = svg.join('');

// ---- header
document.getElementById('title').textContent = DATA.case + ' · ' + DATA.run;
document.getElementById('sub').textContent = `${N} chunks · ${rows.length} items · ${needs.length ? needs.join(', ') : 'no need portrait'}`;
{ const v = DATA.verdict, el = document.getElementById('verdict');
  const groups = {};
  v.forEach(x => { (groups[x.check] = groups[x.check] || []).push(x); });
  el.innerHTML = Object.entries(groups).map(([k, xs]) => { const ok = xs.filter(x=>x.ok).length;
    return `<span class="${ok===xs.length?'pass':'fail'}" title="${esc(xs.map(x=>(x.ok?'PASS ':'FAIL ')+x.what).join('\n'))}">${esc(k)} <b>${ok}/${xs.length}</b></span>`; }).join('');
}

// ---- side panel: the selected chunk as the reader would put it
const DEG = {'very much':'very much','much':'much','somewhat':'somewhat','a little':'a little'};
function side(i){
  const st = S[i], prev = i ? S[i-1] : null;
  const chunk = DATA.chunks[i];
  const att = Object.entries(st.pull).filter(([,p])=>p.sign>0).map(([x,p])=>`<li><span class="att">${esc(x)}</span> <span class="deg">${esc(p.degree)}</span></li>`).join('');
  const rep = Object.entries(st.pull).filter(([,p])=>p.sign<0).map(([x,p])=>`<li><span class="rep">${esc(x)}</span> <span class="deg">${esc(p.degree)}</span></li>`).join('');
  const arrived = st.field.filter(f => !prev || !prev.field.some(g=>g.item===f.item)).map(f=>f.item);
  const left = prev ? prev.field.filter(f => !st.field.some(g=>g.item===f.item)).map(f=>f.item) : [];
  const mind = st.mind.map(m=>`<li>${esc(m.item)} <span class="deg mono">${m.c.toFixed(2)}</span> <span class="deg">${esc(m.why)}</span></li>`).join('');
  const surprises = Object.entries(st.surprise_items).map(([k,xs])=>`<li><em>${esc(k)}</em>: ${esc(xs.join(', '))}</li>`).join('');
  const inst = st.paths.filter(p=>/established/.test(p.note)).map(p=>`<li>${esc(p.item)} → ${esc(p.need)} <span class="mono deg">${p.d>0?'+':''}${p.d}</span></li>`).join('');
  const tail = st.tail;
  document.getElementById('side').innerHTML = `
    <div class="nav"><button id="prev" ${i===0?'disabled':''}>←</button><span class="mono">chunk ${i+1} of ${N}</span><button id="next" ${i===N-1?'disabled':''}>→</button></div>
    ${chunk ? `<h2>the text</h2><p class="chunk">${esc(chunk)}</p>` : ''}
    <h2>what the reader can report</h2>
    <p>Holds ${st.field.length} things in ${st.components ?? '?'} piece${st.components===1?'':'s'}${arrived.length?`; new: ${esc(arrived.join(', '))}`:''}${left.length?`; gone: ${esc(left.join(', '))}`:''}.</p>
    ${att?`<p>Drawn to:</p><ul>${att}</ul>`:''}
    ${rep?`<p>Pushed away by:</p><ul>${rep}</ul>`:''}
    ${st.wants_more?`<p>Wants <b>${esc(st.wants_more.text)}</b> <span class="deg">(${esc(st.wants_more.degree)})</span>.</p>`:''}
    ${st.wants && st.wants!=='-'?`<p>Looking back, wanted: ${esc(st.wants)}.</p>`:''}
    ${st.notices.length?`<p>Has words for itself: <em>${esc(st.notices.join(', '))}</em>.</p>`:''}
    ${st.surprised?`<p>Surprised by itself: ${st.surprised} time${st.surprised===1?'':'s'} this chunk.</p>`:''}
    ${tail.count?`<p>Something nameless in the background: ${tail.valence>0?'pleasant':tail.valence<0?'unpleasant':'neutral'} <span class="mono deg">(valence ${tail.valence.toFixed(2)}, intensity ${(tail.intensity??0).toFixed(2)}, ${tail.count} signals)</span>.</p>`:'<p>Nothing nameless in the background.</p>'}
    <p>${esc(st.does)}; attends to ${esc(st.mode)}${st.ry!=null?` <span class="mono deg">(reality pays ${st.ry.toFixed(2)}, fantasy ${(st.fy??0).toFixed(2)})</span>`:''}.</p>
    <h2>the analyst's view</h2>
    <dl class="kv">
      <dt>program</dt><dd>${esc(st.program)}${st.switches?` · ${st.switches} switch${st.switches===1?'':'es'} so far`:''}</dd>
      <dt>conflict</dt><dd class="mono">${(st.conflict??0).toFixed(2)}</dd>
      <dt>need levels</dt><dd class="mono">${needs.map(n=>`${esc(n)} ${(st.levels[n]??0).toFixed(2)}`).join(' · ')}</dd>
      ${Object.keys(st.mass).length?`<dt>mass in Field</dt><dd class="mono">${Object.entries(st.mass).map(([n,m])=>`${esc(n)} ${m.toFixed(2)}`).join(' · ')}</dd>`:''}
      ${st.levels_summary?`<dt>control levels</dt><dd class="mono">${esc(st.levels_summary)}</dd>`:''}
      ${Object.keys(st.felt).length?`<dt>felt</dt><dd class="mono">${Object.entries(st.felt).map(([f,v])=>`${esc(f)} ${v.toFixed(2)}`).join(' · ')}</dd>`:''}
    </dl>
    ${inst?`<h2>paths the text installed</h2><ul>${inst}</ul>`:''}
    ${st.missing.length?`<h2>prerequisites missing</h2><ul>${st.missing.map(m=>`<li>${esc(m)}</li>`).join('')}</ul>`:''}
    ${mind?`<h2>represented, not conscious</h2><ul>${mind}</ul>`:''}
    ${surprises?`<h2>self-model missed</h2><ul>${surprises}</ul>`:''}
    <h2>trace</h2><div class="trace">${esc(st.trace.join('\n'))}</div>`;
  document.getElementById('prev').onclick = () => select(i-1);
  document.getElementById('next').onclick = () => select(i+1);
}
function select(i){
  if (i<0 || i>=N) return; sel = i;
  document.querySelectorAll('.col').forEach(g => g.classList.toggle('sel', +g.dataset.i===i));
  document.querySelectorAll('.colhead').forEach(g => g.classList.toggle('sel', +g.dataset.i===i));
  side(i);
}
document.querySelectorAll('.col, .colhead').forEach(g => g.addEventListener('click', () => select(+g.dataset.i)));
document.addEventListener('keydown', e => { if (e.key==='ArrowLeft') select(sel-1); if (e.key==='ArrowRight') select(sel+1); });
select(sel);
</script>
"""


def render(run, out):
    page = (PAGE.replace("__TITLE__", html.escape(f"{run['case']} score"))
                .replace("__DATA__", json.dumps(run, ensure_ascii=False).replace("</", "<\\/")))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)


def main(argv):
    args = [a for a in argv if not a.startswith("-")]
    opt = {argv[i]: argv[i + 1] for i, a in enumerate(argv) if a.startswith("-") and i + 1 < len(argv)}
    for v in opt.values():
        if v in args:
            args.remove(v)
    if not args:
        print(__doc__)
        return 2
    run_dir = args[0]
    run = load_run(run_dir, opt.get("--text"), opt.get("--target"))
    out = opt.get("-o") or os.path.join(run_dir, "score.html")
    render(run, out)
    print(f"{out}: {len(run['states'])} states, {len(run['chunks'])} chunks, {len(run['verdict'])} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
