#!/usr/bin/env python3
"""Total numeric columns of a CSV export by group, so no total or ratio is added up by eye.

  python3 sum_by.py export.csv concept                          rows and totals of every numeric column per concept
  python3 sum_by.py export.csv concept spend_usd calls_qualified totals of the named columns only
  python3 sum_by.py export.csv concept --ratio spend_usd/calls_qualified --ratio clicks/impressions

Lines starting with # are ignored. A ratio with a zero denominator prints "n/a (0)", never a number.
Use "-" as the group to total the whole file.
"""
import collections
import csv
import sys
from pathlib import Path


def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", "").replace("%", ""))
    except ValueError:
        return None


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    path, group = Path(args[0]), args[1]
    ratios, cols, rest = [], [], args[2:]
    while rest:
        a = rest.pop(0)
        if a == "--ratio" and rest:
            ratios.append(rest.pop(0).split("/"))
        else:
            cols.append(a)
    lines = [l for l in path.read_text(encoding="utf-8", errors="replace").splitlines()
             if l.strip() and not l.lstrip().startswith("#")]
    rows = list(csv.DictReader(lines))
    if not rows:
        sys.exit("no rows")
    numeric = cols or [c for c in rows[0] if c != group and all(num(r[c]) is not None for r in rows if r[c] != "")
                       and any(r[c] != "" for r in rows)]
    groups = collections.OrderedDict()
    for r in rows:
        key = "ALL" if group == "-" else r.get(group, "")
        g = groups.setdefault(key, {"rows": 0, **{c: 0.0 for c in numeric}})
        g["rows"] += 1
        for c in numeric:
            g[c] += num(r.get(c)) or 0.0
    total = {"rows": sum(g["rows"] for g in groups.values()), **{c: sum(g[c] for g in groups.values()) for c in numeric}}
    if group != "-":
        groups["TOTAL"] = total
    fmt = lambda x: f"{x:,.0f}" if float(x).is_integer() else f"{x:,.2f}"
    for key, g in groups.items():
        parts = [f"rows {g['rows']}"] + [f"{c} {fmt(g[c])}" for c in numeric]
        for a, b in ratios:
            if a in g and b in g:
                parts.append(f"{a}/{b} " + (fmt(g[a] / g[b]) if g[b] else "n/a (0)"))
        print(f"{key}: " + ", ".join(parts))


if __name__ == "__main__":
    main()
