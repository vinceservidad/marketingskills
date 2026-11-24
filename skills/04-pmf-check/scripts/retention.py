#!/usr/bin/env python3
"""Customer (logo) retention from a customer log with a start and an optional end month.

  python3 retention.py clients.csv 2026-10                      as-of month (customers with no end are active)
  python3 retention.py clients.csv 2026-10 segment              also split by a column

Columns: start_month and end_month (YYYY-MM; blank end = still a customer). Rows starting with # are ignored.
Prints, per start-year cohort: customers, still active, and retention at 3, 6, 12 and 24 months counted only
over customers old enough to have reached that age (the denominator is shown). Also tenure to date: median over
all customers and over customers who started at least 12 months before the as-of month. Active customers'
tenure is still growing (censored), so a median tenure is not a lifetime.
"""
import collections
import csv
import sys
from pathlib import Path


def months(s):
    y, m = map(int, s.strip()[:7].split("-"))
    return y * 12 + m


def median(xs):
    xs = sorted(xs)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def table(label, rows, asof):
    print(f"\n{label}: {len(rows)} customers, {sum(not r['end_month'].strip() for r in rows)} active at {asof}")
    cohorts = collections.defaultdict(list)
    for r in rows:
        cohorts[r["start_month"][:4]].append(r)
    a = months(asof)
    for age in (3, 6, 12, 24):
        line = []
        for y in sorted(cohorts):
            eligible = [r for r in cohorts[y] if a - months(r["start_month"]) >= age]
            kept = [r for r in eligible if not r["end_month"].strip() or months(r["end_month"]) - months(r["start_month"]) >= age]
            line.append(f"{y} {len(kept)}/{len(eligible)}" if eligible else f"{y} too young")
        print(f"  retained at {age} months: " + "; ".join(line))
    tenure = [(months(r["end_month"]) if r["end_month"].strip() else a) - months(r["start_month"]) for r in rows]
    old = [t for r, t in zip(rows, tenure) if a - months(r["start_month"]) >= 12]
    print(f"  tenure to date (months): median all {median(tenure)} (n={len(tenure)}); "
          f"median of customers started 12+ months ago {median(old)} (n={len(old)})")
    ended = [r for r in rows if r["end_month"].strip()]
    if ended:
        reasons = collections.Counter(r.get("reason_left", "").strip() or "(no reason)" for r in ended)
        print("  ended: " + "; ".join(f"{k} {v}" for k, v in reasons.most_common()))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    path, asof = Path(sys.argv[1]), sys.argv[2]
    lines = [l for l in path.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip() and not l.lstrip().startswith("#")]
    rows = list(csv.DictReader(lines))
    table("all", rows, asof)
    if len(sys.argv) > 3:
        by = sys.argv[3]
        groups = collections.defaultdict(list)
        for r in rows:
            groups[r.get(by, "")].append(r)
        for g in sorted(groups):
            table(f"{by}={g}", groups[g], asof)


if __name__ == "__main__":
    main()
