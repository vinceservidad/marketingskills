#!/usr/bin/env python3
"""Score brand assets on fame and uniqueness from recognition-survey counts, so no percentage is computed by eye.

  python3 asset_grid.py survey.csv
  python3 asset_grid.py survey.csv --brand named_ourbrand --other named_other_brand --base respondents

The CSV needs one row per asset with: the asset name, the number of respondents, how many named our brand,
and how many named another brand. Lines starting with # are ignored. Column names are detected when they are
`asset`, `respondents`, a `named_<brand>` column and a `named_other...` column; otherwise pass them.

  fame       = named our brand / respondents
  uniqueness = named our brand / (named our brand + named another brand)   (n/a when nobody named any brand)

Quadrants use the heuristic 50% cut-offs from Romaniuk's Distinctive Asset Grid (Building Distinctive Brand
Assets, 2018). They are a rule of thumb, not a law: report the numbers and the sample with every label.
"""
import argparse
import csv
import sys
from pathlib import Path


def quadrant(fame, uniq):
    if uniq is None:
        return "no attribution yet (unknown)"
    if fame >= 0.5 and uniq >= 0.5:
        return "use or lose (strong: protect and use everywhere)"
    if fame < 0.5 and uniq >= 0.5:
        return "investment potential (unique but not yet known: build fame)"
    if fame >= 0.5 and uniq < 0.5:
        return "avoid solo use (known but shared with others: pair with the name)"
    return "ignore or test (neither known nor unique)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--asset", default="asset")
    ap.add_argument("--base", default="respondents")
    ap.add_argument("--brand")
    ap.add_argument("--other")
    a = ap.parse_args()
    lines = [l for l in Path(a.csv).read_text(encoding="utf-8").splitlines() if l.strip() and not l.lstrip().startswith("#")]
    rows = list(csv.DictReader(lines))
    if not rows:
        sys.exit("no rows")
    cols = list(rows[0])
    other = a.other or next((c for c in cols if c.startswith("named_other")), None)
    brand = a.brand or next((c for c in cols if c.startswith("named_") and c != other), None)
    if not (brand and other and a.base in cols and a.asset in cols):
        sys.exit(f"could not find columns; have {cols}. Pass --asset, --base, --brand and --other.")
    print(f"brand column: {brand}; other-brand column: {other}; base: {a.base}")
    print("| Asset | Base | Named us | Named another brand | Fame | Uniqueness | Grid position |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        n, us, oth = int(r[a.base]), int(r[brand]), int(r[other])
        fame = us / n if n else 0.0
        uniq = us / (us + oth) if us + oth else None
        u = f"{uniq:.0%} ({us}/{us + oth})" if uniq is not None else "n/a"
        pos = quadrant(fame, uniq)
        if uniq is not None and us + oth < 10:
            pos += "; uniqueness rests on fewer than 10 attributions, too few to rely on"
        print(f"| {r[a.asset]} | {n} | {us} | {oth} | {fame:.0%} ({us}/{n}) | {u} | {pos} |")
    print("\nCut-offs are heuristic (50%). State the sample, who was asked and how before drawing conclusions.")


if __name__ == "__main__":
    main()
