#!/usr/bin/env python3
"""Sum a step-by-step funnel export exactly and compute each step's rate, overall and by group.

  python3 funnel.py export.csv                       totals and step rates over all rows
  python3 funnel.py export.csv staff_band            also per value of a column (segment, plan, band)
  python3 funnel.py export.csv signup_month --exclude 2026-09    drop rows whose any field equals a value
                                                     (for example an incomplete cohort)

The numeric columns, in file order, are the funnel steps. Rows starting with # are ignored. For each step it
prints the count, the rate from the previous step and the rate from the first step, with numerator and
denominator, so no rate is computed by eye.
"""
import collections
import csv
import sys
from pathlib import Path


def is_num(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def show(label, rows, steps):
    tot = [sum(float(r[s]) for r in rows) for s in steps]
    out = []
    for i, (s, v) in enumerate(zip(steps, tot)):
        v_s = f"{v:g}"
        if i == 0:
            out.append(f"{s} {v_s}")
        else:
            prev, first = tot[i - 1], tot[0]
            p = f"{v / prev:.1%}" if prev else "n/a"
            f = f"{v / first:.1%}" if first else "n/a"
            out.append(f"{s} {v_s} ({v_s}/{tot[i - 1]:g} = {p} of previous; {f} of {steps[0]})")
    print(f"{label} [{len(rows)} rows]: " + " → ".join(out))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    args = sys.argv[2:]
    exclude = []
    if "--exclude" in args:
        i = args.index("--exclude")
        exclude = args[i + 1:]
        args = args[:i]
    path = Path(sys.argv[1])
    lines = [l for l in path.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip() and not l.lstrip().startswith("#")]
    rows = list(csv.DictReader(lines))
    rows = [r for r in rows if not any(v in exclude for v in r.values())]
    if not rows:
        sys.exit("no rows")
    steps = [c for c in rows[0] if all(is_num(r[c]) for r in rows)]
    if exclude:
        print(f"excluded rows with: {', '.join(exclude)}")
    show("all", rows, steps)
    for by in args:
        groups = collections.defaultdict(list)
        for r in rows:
            groups[r.get(by, "")].append(r)
        for g in groups:
            show(f"{by}={g}", groups[g], steps)


if __name__ == "__main__":
    main()
