#!/usr/bin/env python3
"""Gellish English dictionary (gellish.net CSV release, July 2020) -> Soufflé fact files.

Usage: python -m nous.gellish.dictionary <dictionary-dir> [extra.csv ...] -o <facts-dir>   (normally via `nous gellish build-dict`)

The CSVs are semicolon-separated; row 1 carries stable column-role UIDs (2 = left UID,
60 = relation UID, 15 = right UID, ...) which we use instead of the (varying) header names.
Numbers may carry Excel thousand separators ("4.289").

Emits:
  d_concept.facts   uid  name                       primary name per UID
  d_spec.facts      sub  super  kind                1146 is a kind of / 1726 qualitative subtype
  d_alias.facts     name  uid  kind                 1981 synonym, 1982 abbreviation, 1984 noun form, 5668 infinitive, 6523 gerund
  d_phrase.facts    phrase  rel_uid  dir            6066 base phrase / 1986 inverse phrase (dir = base|inv)
  d_role.facts      rel_uid  pos  role_uid          5944 first role / 5945 second role
  d_role_of.facts   role_uid  kind_uid              5343 is by definition a role of a
  d_def.facts       uid  definition                 full definition text
  d_class.facts     ind_uid  kind_uid                1225 classification of individuals
  d_fact.facts      l  rel  r  coll                  every other dictionary-level fact (used for grounded entities only)
  d_coll.facts      uid  collection_uid              which collection (dictionary / extension) defines a concept
  d_name_lc.facts   uid  lowercased name            for grounding document entities
  d_relname.facts   rel_uid  phrase                  one canonical base phrase per relation type
"""
import argparse, csv, glob, os, pathlib, re, sys

COL = {'int': '43', 'l': '2', 'ln': '101', 'rel': '60', 'reln': '3', 'r': '15', 'rn': '201', 'fdef': '4', 'pdef': '65', 'coll': '50'}


def uid(s):
    s = s.strip().replace('.', '').replace(',', '')
    return s if s.isdigit() else ''


def load(paths):
    out = []
    files = []
    for d in paths:
        files += sorted(glob.glob(os.path.join(d, '*.csv'))) if os.path.isdir(d) else [d]
    for f in files:
        with open(f, encoding='utf-8-sig', errors='replace') as fh:
            rows = list(csv.reader(fh, delimiter=';'))
        codes = [c.strip() for c in rows[1]]
        idx = {k: codes.index(v) for k, v in COL.items() if v in codes}
        for r in rows[3:]:
            if len(r) < len(codes) - 3:
                continue
            g = lambda k: r[idx[k]].strip() if k in idx and idx[k] < len(r) else ''
            rec = {k: g(k) for k in COL}
            for k in ('l', 'r', 'rel', 'coll'):
                rec[k] = uid(rec[k])
            out.append(rec)
    return out


def clean(s):
    return re.sub(r'\s+', ' ', s).strip().replace('\t', ' ')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('sources', nargs='+', help='dictionary directory and/or extra CSV files (e.g. ext/philosophy_of_mind.csv)')
    ap.add_argument('-o', '--out', default='facts')
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    R = load(a.sources)

    concept, spec, alias, phrase, role, role_of, defs = {}, set(), set(), {}, set(), set(), {}
    cls, dfact, coll = set(), set(), {}
    STRUCT = {'1146', '1726', '6066', '1986', '1981', '1982', '1984', '5668', '6523', '5944', '5945', '5343', '1225'}
    for d in R:
        l, r, rel = d['l'], d['r'], d['rel']
        ln, rn = clean(d['ln']), clean(d['rn'])
        if not l:
            continue
        if rel in ('1146', '1726'):
            concept.setdefault(l, ln)          # the defining row names the concept
            if d['coll']:
                coll.setdefault(l, d['coll'])
            if r:
                spec.add((l, r, rel))
                concept.setdefault(r, rn)
        if rel == '6066' and r:
            phrase.setdefault((ln.lower(), r, 'base'), None)
        elif rel == '1986' and r:
            phrase.setdefault((ln.lower(), r, 'inv'), None)
        elif rel in ('1981', '1982', '1984', '5668', '6523') and r:
            alias.add((ln.lower(), r, rel))
        elif rel in ('5944', '5945') and r:
            role.add((l, '1' if rel == '5944' else '2', r))
            concept.setdefault(r, rn)
        elif rel == '5343' and r:
            role_of.add((l, r))
            concept.setdefault(r, rn)
        elif rel == '1225' and r:
            cls.add((l, r)); concept.setdefault(l, ln); concept.setdefault(r, rn)
            if d['coll']:
                coll.setdefault(l, d['coll'])
        elif rel and r and rel not in STRUCT:
            dfact.add((l, rel, r, d['coll'])); concept.setdefault(l, ln); concept.setdefault(r, rn)
        fd = clean(d['fdef']) or clean(d['pdef'])
        if fd and l not in defs and rel in ('1146', '1726'):
            defs[l] = fd
    for d in R:                                # names for anything still unnamed
        if d['l'] and d['l'] not in concept and d['ln']:
            concept[d['l']] = clean(d['ln'])

    def dump(name, rows):
        with (out / name).open('w') as f:
            for row in sorted(rows):
                f.write('\t'.join(row) + '\n')

    dump('d_concept.facts', concept.items())
    dump('d_spec.facts', spec)
    dump('d_alias.facts', alias)
    dump('d_phrase.facts', phrase)
    dump('d_role.facts', role)
    dump('d_role_of.facts', role_of)
    dump('d_def.facts', defs.items())
    dump('d_class.facts', cls)
    dump('d_fact.facts', dfact)
    dump('d_coll.facts', coll.items())
    dump('d_name_lc.facts', ((u, n.lower()) for u, n in concept.items()))
    relname = {}
    for ph, u, d in phrase:                    # first-declared base phrase names the relation type
        if d == 'base':
            relname.setdefault(u, ph)
    dump('d_relname.facts', relname.items())
    print(f"{len(R)} rows -> {len(concept)} concepts, {len(spec)} specialisations, {len(phrase)} phrases, "
          f"{len(alias)} aliases, {len(role)} role defs, {len(role_of)} role players, {len(defs)} definitions",
          file=sys.stderr)


if __name__ == '__main__':
    main()
