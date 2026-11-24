#!/usr/bin/env python3
"""List every quotation in a draft that does not appear word for word in the sources.

  python3 check_quotes.py context/message.md                # sources: inputs/ and the other context/ files
  python3 check_quotes.py draft.md inputs/notes.md ...       # explicit sources

Prints each unmatched quotation; exit 1 if any. Fix each one before saving: copy the exact words from the
source, or drop the quotation marks and put your own wording in italics.
"""
import re
import sys
from pathlib import Path

QUOTE = re.compile(r"\"([^\"\n]*)\"|“([^”\n]*)”")


def norm(text):
    text = text.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[—–]", "-", text)
    return re.sub(r"\s+", " ", text).strip(" .,;:!?-'\"")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    draft = Path(sys.argv[1])
    sources = [Path(p) for p in sys.argv[2:]]
    if not sources:
        sources = [p for p in Path("inputs").rglob("*") if p.is_file()] if Path("inputs").is_dir() else []
        sources += [p for p in Path("context").glob("*.md") if p.resolve() != draft.resolve()]
    corpus = norm(" ".join(p.read_text(encoding="utf-8", errors="replace") for p in sources))
    bad = []
    for m in QUOTE.finditer(draft.read_text(encoding="utf-8")):
        q = m.group(1) if m.group(1) is not None else m.group(2)
        if len(q.split()) < 4:
            continue
        parts = [p for p in re.split(r"\.\.\.|…|\[[^\]]*\]", q) if len(p.split()) >= 2]
        if not all(norm(p) in corpus for p in parts):
            bad.append(q)
    for q in bad:
        print(f'not in any source: "{q}"')
    print(f"{len(bad)} unmatched quotation(s)." if bad else "Every quotation matches a source.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
