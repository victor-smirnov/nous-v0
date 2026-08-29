"""Pipelines: build the dictionary facts, run the reasoner, explain."""
import importlib.util, io, shutil, subprocess, sys, urllib.request, zipfile

from . import dictionary, parse, paths, report


# ------------------------------------------------------------------ dictionary + extensions
def load_specs():
    """ext/<name>/spec.py modules in dependency order."""
    mods = {}
    for d in sorted(paths.EXT.iterdir()):
        f = d / "spec.py"
        if f.exists():
            s = importlib.util.spec_from_file_location(f"ext_{d.name}", f)
            m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
            mods[getattr(m, "NAME", d.name)] = m
    order, seen = [], set()

    def visit(n):
        if n in seen:
            return
        for dep in getattr(mods[n], "DEPENDS", []):
            visit(dep)
        seen.add(n); order.append(n)
    for n in mods:
        visit(n)
    return [(n, mods[n]) for n in order]


def build_extensions(out_dir):
    """Run every spec; write <name>.csv into out_dir plus sem.facts / disjoint_rel.facts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    built, sem, disjoint = {}, [], []
    for name, mod in load_specs():
        deps = {d: built[d] for d in getattr(mod, "DEPENDS", [])}
        e = mod.build(out_dir, deps)
        built[name] = e
        sem += e.sem; disjoint += e.disjoint
    with (out_dir / "sem.facts").open("w") as f:
        for u, t in sem:
            f.write(f"{u}\t{t}\n")
    with (out_dir / "disjoint_rel.facts").open("w") as f:
        for a, b in disjoint:
            f.write(f"{a}\t{b}\n")
    return [out_dir / f"{n}.csv" for n in built]


def build_dict(ws, fetch=False):
    if fetch or not ws.dict.exists() or not any(ws.dict.glob("*.csv")):
        ws.dict.mkdir(parents=True, exist_ok=True)
        print(f"fetching {paths.DICT_URL}", file=sys.stderr)
        data = urllib.request.urlopen(paths.DICT_URL, timeout=300).read()
        (ws.dict / "dict2020.zip").write_bytes(data)
        zipfile.ZipFile(io.BytesIO(data)).extractall(ws.dict)
    ext_dir = ws.dictfacts / "ext"
    csvs = build_extensions(ext_dir)
    dictionary.main([str(ws.dict), *map(str, csvs), "-o", str(ws.dictfacts)])
    for n in ("sem.facts", "disjoint_rel.facts"):
        shutil.copy(ext_dir / n, ws.dictfacts / n)


# ------------------------------------------------------------------ reasoning
def check(ws, tables, minlevel=2, maxdepth=8, theory="hypothesis", disjoint=None, jobs="auto", quiet=False):
    paths.require_souffle(); ws.require_dictfacts()
    ws.fresh()
    for f in ws.dictfacts.glob("*.facts"):
        shutil.copy(f, ws.facts / f.name)
    argv = [*tables, "-o", str(ws.facts), "--minlevel", str(minlevel), "--maxdepth", str(maxdepth), "--theory", theory]
    if disjoint:
        argv += ["--disjoint", disjoint]
    parse.main(argv)
    r = subprocess.run(["souffle", "-j", str(jobs), "-F", str(ws.facts), "-D", str(ws.out), str(ws.reasoner)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr)
    for line in r.stderr.splitlines():
        if "Warning" in line and not quiet:
            print(line, file=sys.stderr)
    return report.render(ws.out, ws.facts)
