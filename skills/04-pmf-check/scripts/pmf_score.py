#!/usr/bin/env python3
"""Score a Sean Ellis survey exactly: share answering "Very disappointed", overall and by group.

  python3 pmf_score.py survey.csv                         auto-detects the disappointment column
  python3 pmf_score.py survey.csv q1_disappointment segment   answer column, then a column to split by

Rows starting with # are ignored. Answers like "N/A", "no longer use" or blank are excluded from the
denominator and counted separately. Prints n, counts per answer, the very-disappointed share and a 95%
Wilson interval, so a small sample is visible. The 40% line is Ellis's heuristic, not a law: report the
number and its n, never "PMF achieved" from the score alone.
"""
import collections
import csv
import math
import sys
from pathlib import Path


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def excluded(a):
    a = a.strip().lower()
    return not a or a.startswith("n/a") or "no longer" in a or a == "na"


def report(label, answers):
    valid = [a for a in answers if not excluded(a)]
    n = len(valid)
    very = sum(a.strip().lower().startswith("very") for a in valid)
    counts = collections.Counter(a.strip() for a in answers)
    lo, hi = wilson(very, n)
    share = f"{very}/{n} = {very / n:.0%}" if n else "0/0"
    print(f"{label}: n={n} (excluded {len(answers) - n}); very disappointed {share}; 95% interval {lo:.0%} to {hi:.0%}; "
          + ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    lines = [l for l in path.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip() and not l.lstrip().startswith("#")]
    rows = list(csv.DictReader(lines))
    if not rows:
        sys.exit("no rows")
    col = sys.argv[2] if len(sys.argv) > 2 else next((c for c in rows[0] if "disappoint" in c.lower()), None)
    if not col:
        sys.exit("name the answer column: python3 pmf_score.py survey.csv <column> [group column]")
    report("all", [r[col] for r in rows])
    if len(sys.argv) > 3:
        by = sys.argv[3]
        groups = collections.defaultdict(list)
        for r in rows:
            groups[r.get(by, "")].append(r[col])
        for g in sorted(groups):
            report(f"{by}={g}", groups[g])


if __name__ == "__main__":
    main()
