#!/usr/bin/env python3
"""Fill the board template with one pyramid.

Usage: pyramid_board.py <pyramid.json> <out.html>

Writes the board, then checks the pyramid's structure and reports. It never
changes the pyramid: a problem is reported, and the board is still drawn so the
gap shows.
"""
import json
import sys
from pathlib import Path

KINDS = {"examples", "numbers", "steps", "quotes", "questions", "comparisons"}
MEDIA = {"page", "deck", "email", "document"}
REQUIRED = ["piece", "reader", "question", "answer", "claims"]


def check(p):
    notes = []
    for key in REQUIRED:
        if not p.get(key):
            notes.append(f"missing: {key}")
    if p.get("medium", "page") not in MEDIA:
        notes.append(f"unknown medium: {p.get('medium')}")
    if p.get("opening", "cold") not in {"cold", "asked"}:
        notes.append(f"unknown opening: {p.get('opening')}")
    claims = p.get("claims") or []
    if not 2 <= len(claims) <= 5:
        notes.append(f"{len(claims)} claims; a pyramid holds two to five")
    for i, claim in enumerate(claims, 1):
        if claim.get("support_kind") not in KINDS:
            notes.append(f"claim {i}: unknown kind of support: {claim.get('support_kind')}")
        support = claim.get("support") or []
        invented = sum(1 for item in support if item.get("source") == "invented")
        if not support:
            notes.append(f"claim {i}: no proof yet")
        elif invented:
            notes.append(f"claim {i}: {invented} invented, not proof")
    return notes


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    source, out = Path(sys.argv[1]), Path(sys.argv[2])
    pyramid = json.loads(source.read_text(encoding="utf-8"))
    template = (Path(__file__).resolve().parent.parent / "assets" / "pyramid-board.html").read_text(encoding="utf-8")
    data = json.dumps(pyramid, ensure_ascii=False).replace("</", "<\\/")
    out.write_text(template.replace("__PYRAMID_JSON__", data), encoding="utf-8")
    notes = check(pyramid)
    print(f"board written: {out} ({out.stat().st_size} bytes)")
    print("structure: " + ("ok" if not notes else "; ".join(notes)))


if __name__ == "__main__":
    main()
