#!/usr/bin/env python3
"""Count items exactly, so no number in the context file is counted by eye.

  python3 tally.py reviews.csv                   rows, and counts for every column with few distinct values
  python3 tally.py reviews.csv stars source      counts for the named columns
  python3 tally.py notes.md 'R\\d+|T-\\d+|I-\\d+'   distinct item IDs matching a pattern, per prefix
"""
import collections
import csv
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
args = sys.argv[2:]
text = path.read_text(encoding="utf-8", errors="replace")
if path.suffix.lower() in (".csv", ".tsv"):
    lines = [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    rows = list(csv.DictReader(lines, delimiter="\t" if path.suffix.lower() == ".tsv" else ","))
    print(f"{len(rows)} rows")
    cols = args or [c for c in rows[0] if 1 < len({r[c] for r in rows}) <= 12] if rows else []
    for c in cols:
        counts = collections.Counter(r.get(c, "") for r in rows)
        print(f"{c}: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))))
else:
    pattern = re.compile(args[0] if args else r"\b[A-Z]{1,3}-?\d{1,5}\b")
    ids = sorted(set(pattern.findall(text)))
    by_prefix = collections.Counter(re.sub(r"\d+$", "", i) for i in ids)
    print(f"{len(ids)} distinct IDs: " + ", ".join(f"{k}* {v}" for k, v in sorted(by_prefix.items())))
