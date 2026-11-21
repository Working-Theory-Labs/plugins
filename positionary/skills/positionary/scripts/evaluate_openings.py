#!/usr/bin/env python3
"""Lay out the closer look at openings that were read in full.

Usage:  python3 evaluate_openings.py evaluated.json      (or JSON on stdin)

The rating is the reader's judgment and is passed in. This script sets out
the table the same way every time, and works out the owner's own hours and,
when their settings give the figures, their floor and their cost for the turn
that follows.

Input: {"settings": {...}, "openings": [{...}, ...]}

  settings (all optional)
    weekly_cost      what an unbooked week costs the owner, from their
                     venue settings; omit when they have given none
    week_hours       the hours in the owner's working week          default 40
    floor_rate       the least an hour of the owner's time may earn, from
                     their venue settings; omit when they have given none
    venue_fee        the share of the price the venue keeps         default 0.10
    hours_by_kind    {kind of work: the owner's own hours a week}; default 5
                     for every kind

  opening
    n, name          its number and short name from the table
    work_kind, weeks as in the table
    low, high        the buyer's range after the full read: the budget the
                     post names when it names one, else the table's range.
                     Give the same figure twice when the buyer states one.
    owner_hours      the owner's own hours on the whole job, when they say;
                     else weeks x the hours for its kind
    rating           "great" or "good"
    why              the reason for the rating, in eight words or fewer

Worked out for each opening:
  Human Hours   owner_hours
  Floor         owner_hours x floor_rate. The owner does not go under it.
                null when no floor_rate was given.
  Cost          owner_hours x (weekly_cost / week_hours) / (1 - venue_fee).
                null when no weekly_cost was given.

No price is worked out here. The owner sets the price when the proposal is
built, and may set it under or over the buyer's range.
"""
import json
import sys


def money(x):
    return "${:,.0f}".format(round(x / 10) * 10)


def main():
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = json.load(src)
    s = data.get("settings") or {}
    out = []
    print("| # | Opening | Est. Value | Rating | Why |")
    print("|---|---|---|---|---|")
    for o in data["openings"]:
        hours = o.get("owner_hours")
        if hours is None:
            hours = o["weeks"] * (s.get("hours_by_kind") or {}).get(o.get("work_kind"), 5)
        est = money(o["high"]) if o["low"] == o["high"] else "{} to {}".format(
            money(o["low"]), money(o["high"]))
        words = str(o.get("why") or "").split()
        print("| {} | {} | {} | {} | {} |".format(
            o["n"], o["name"], est, "Great" if o.get("rating") == "great" else "Good",
            " ".join(words[:8])))
        rate, week = s.get("floor_rate"), s.get("weekly_cost")
        out.append({"n": o["n"], "name": o["name"], "range": est, "human_hours": hours,
                    "floor": money(hours * rate) if rate else None,
                    "cost": money(hours * week / s.get("week_hours", 40)
                                  / (1 - s.get("venue_fee", 0.10))) if week else None})
    print()
    print(json.dumps(out))


if __name__ == "__main__":
    main()
