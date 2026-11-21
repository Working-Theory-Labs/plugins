#!/usr/bin/env python3
"""List a venue's best openings as fixed-price bids, in one table.

Usage:  python3 rank_openings.py openings.json      (or JSON on stdin)

Every opening gets a value with no help from the owner, and the same rules
apply to every row. If this script cannot be run, apply the rules below by
hand, in this order, and say that the table was worked out by hand.

Input: {"settings": {...}, "openings": [{...}, ...]}

  settings (all optional)
    levels           leverage levels to show          default: ["sweet"]
                     when the owner's list holds a sweet kind, else ["good"],
                     which with no list is every opening
    max_rows         most rows in the table                        default 5
    sort             "value" or "fastest"                          default "value"
    floor            smallest Est. Value shown                     default 0
    max_age_days     oldest post shown, in days since it was published
                                                                   default 30
    cap_weeks        most weekly milestones one bid holds          default 4
    fallback_rate    hourly rate when nothing else gives one       default 40
    leverage         the owner's own kinds of work, from their venue
                     settings: {kind of work: "sweet" | "good" | "poor"}.
                     Omit it when the owner has none
    today            the date, as YYYY-MM-DD, for working out a post's age

  opening
    id, name         the venue's id, and the short name for the table
    work_kind        the one kind of work, from the owner's list, that the
                     post mostly asks for; "other" when none fits; omit when
                     the owner has no list
    job_type         "fixed" or "hourly", as the listing gives it
    budget           the listing's budget, copied exactly, such as
                     "15.00–30.00/hr" or "$1,400"; omit when it gives none
    engagement       the listing's workload, copied exactly: "PART_TIME" or
                     "FULL_TIME"
    duration         the listing's length, copied exactly, such as
                     "Less than 1 month" or "3 to 6 months"
    published        the listing's published date, copied exactly
    buyer_avg_rate   the buyer's average hourly rate paid, when the listing shows it

    description      the post's description, copied exactly and whole, as the
                     listing returned it; omit when the listing gives none

  Copy these from the listing and nothing else. Do not read the description
  yourself for a budget, an hourly rate or a length at this step: pass it
  whole and this script reads it, by rule 6a, so a post ranks alike on
  every run.
    work             false when the owner's record does not show this kind of work
    preferred_buyer  true when the post is from a kind of buyer the owner's
                     settings say they prefer; omit otherwise

Kinds of work are the owner's own, and this script holds none. Leverage is
how much of a job the owner's own system does, and what the job leads to:
"sweet", "good" or "poor". A kind the owner's list does not hold is "good".
With no list there is no leverage: every opening is ranked by value alone.

The rules
  1. An opening with work == false is left out, and so is one published
     more than max_age_days ago. A post with no published date is kept.
  2. Leverage: the level of its work_kind in the owner's list. Only the
     levels in `levels` are shown; the rest are counted by level. With no
     list, every opening is shown.
  2a. A preferred buyer lifts an opening one level: poor to good, good to
     sweet. It leaves no opening out and changes no value. With no list
     there are no levels to lift.
  3. Rate (hourly only): the midpoint of the budget's range, or its one
     figure; else the buyer's average rate paid; else the median rate of
     this run's other hourly openings; else fallback_rate.
  4. Hours a week: PART_TIME -> 15, FULL_TIME -> 35; else 15.
  5. Weeks: a duration of less than a week -> 1; less than a month -> 3;
     anything longer -> cap_weeks. A fixed job with no duration: one week
     for each $2,000 of budget, rounded up, cap_weeks at most. An hourly job
     with no duration: cap_weeks.
  6. Est. Value is a range: fixed -> the budget's one figure, since the
     buyer stated it. Hourly -> the low and the high of the budget's range,
     each x hours a week x weeks; when the budget gives one rate or none,
     the rate of rule 3 gives one figure. An opening whose top figure is
     under the floor is left out, and so is a fixed job with no budget.
  6a. A budget the buyer wrote in the description replaces rule 6's figure,
     whatever the listing says: the first place the word "budget" is
     followed in the same sentence, within 40 characters, by a dollar
     figure or a dollar range, or
     a dollar figure or range is followed directly by "budget". A figure
     per hour, per week or per month is not a budget, and neither is an ad,
     advertising, marketing or media budget. One figure is one value; a
     range is its low and high. With no duration, weeks follow rule 5's
     fixed-job rule on the top figure.
  7. Order by value: the top of the range, highest first; then id.
  8. Pays In: one week to be hired, a week for the first milestone, then a
     week for approval and the venue's hold; rounded up to
     whole weeks. Order by fastest: Pays In, shortest first; then the newest
     post; then Est. Value, highest first.
  9. The table holds the first max_rows; the rest are counted.
"""
import json
import math
import re
import statistics
import sys
from datetime import date

WORKLOAD = {"PART_TIME": 15, "FULL_TIME": 35}


def figures(o):
    """The numbers in the listing's budget, in the order written."""
    text = str(o.get("budget") or "").replace(",", "")
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]


def is_hourly(o):
    return o.get("job_type") == "hourly" or "/hr" in str(o.get("budget") or "")


def posted_rate(o):
    f = figures(o)
    return sum(f[:2]) / len(f[:2]) if f else None


_MONEY = r"\$\s?(\d[\d,]*(?:\.\d+)?)\s?(k\b)?"
_RANGE = _MONEY + r"(?:\s*(?:-|–|—|to)\s*" + _MONEY + r")?"
_STATED = [
    re.compile(r"(?P<lead>\b\w+\s+)?\bbudget\b[^$\n.!?]{0,40}?" + _RANGE + r"(?P<tail>[^\n]{0,12})", re.I),
    re.compile(r"(?P<lead>)" + _RANGE + r"\s+budget\b(?P<tail>)", re.I),
]
_NOT_A_JOB_BUDGET = {"ad", "ads", "advertising", "marketing", "media"}
_PER_PERIOD = re.compile(r"^\s*(/|per\b|an?\b|each\b)\s*(hr|hour|week|wk|month|mo)\b", re.I)


def stated_budget(o):
    """The (low, high) budget the buyer wrote in the description, by rule 6a, or None."""
    text = str(o.get("description") or "")
    found = []
    for pattern in _STATED:
        for m in pattern.finditer(text):
            if (m.group("lead") or "").strip().lower() in _NOT_A_JOB_BUDGET:
                continue
            if _PER_PERIOD.match(m.group("tail") or ""):
                continue
            nums = [g for g in m.groups()[1:5]]
            pairs = [(nums[0], nums[1]), (nums[2], nums[3])]
            values = [float(n.replace(",", "")) * (1000 if k else 1) for n, k in pairs if n]
            found.append((m.start(), min(values), max(values)))
    if not found:
        return None
    _, low, high = min(found)
    return low, high


def price_out(o, s, posted):
    """Return (low, high, weeks) for one opening, by rules 3 to 6a."""
    cap = int(s.get("cap_weeks", 4))
    d = str(o.get("duration") or "").lower()
    weeks = None
    if "week" in d and "less" in d:
        weeks = 1
    elif "less than 1 month" in d:
        weeks = 3
    elif d:
        weeks = cap
    stated = stated_budget(o)
    if stated:
        low, high = stated
        if weeks is None:
            weeks = math.ceil(high / 2000)
        return low, high, max(1, min(cap, weeks))
    if not is_hourly(o):
        f = figures(o)
        if not f:
            return None, None, None
        value = f[0]
        if weeks is None:
            weeks = math.ceil(value / 2000)
        return value, value, max(1, min(cap, weeks))
    mine = posted_rate(o)
    others = list(posted)
    if mine in others:
        others.remove(mine)
    rate = (mine or o.get("buyer_avg_rate")
            or (statistics.median(others) if others else None)
            or s.get("fallback_rate", 40))
    weeks = min(cap, weeks if weeks is not None else cap)
    per_rate = WORKLOAD.get(o.get("engagement"), 15) * weeks
    f = figures(o)
    if len(f) >= 2:
        return min(f[:2]) * per_rate, max(f[:2]) * per_rate, weeks
    return rate * per_rate, rate * per_rate, weeks


def rank(data):
    s = data.get("settings") or {}
    leverage = s.get("leverage") or {}
    levels = s.get("levels") or (["sweet"] if "sweet" in leverage.values() else ["good"])
    today = date.fromisoformat(s["today"]) if s.get("today") else date.today()
    openings = [o for o in data["openings"] if o.get("work", True)]
    posted = [r for r in (posted_rate(o) for o in openings if is_hourly(o)) if r]
    rows, held, unplaced = [], {}, []
    for o in openings:
        work_kind = o.get("work_kind") or "other"
        level = leverage.get(work_kind, "good")
        if leverage and o.get("preferred_buyer"):
            level = {"poor": "good", "good": "sweet"}.get(level, level)
        if level not in levels:
            held[level] = held.get(level, 0) + 1
            continue
        low, value, weeks = price_out(o, s, posted)
        if value is None or value < s.get("floor", 0):
            continue
        pays_in = 3
        if leverage and (work_kind == "other" or work_kind not in leverage):
            unplaced.append(o["name"])
        age = (today - date.fromisoformat(o["published"][:10])).days if o.get("published") else 999
        if o.get("published") and age > s.get("max_age_days", 30):
            continue
        rows.append({"id": o.get("id"), "name": o["name"], "low": low, "value": value,
                     "weeks": weeks, "pays_in": pays_in, "age": age})
    if s.get("sort") == "fastest":
        rows.sort(key=lambda r: (r["pays_in"], r["age"], -r["value"], str(r["id"])))
    else:
        rows.sort(key=lambda r: (-r["value"], str(r["id"])))
    return rows, held, unplaced


def money(x):
    return "${:,.0f}".format(round(x / 10) * 10)


def main():
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = json.load(src)
    s = data.get("settings") or {}
    rows, held, unplaced = rank(data)
    shown = rows[:int(s.get("max_rows", 5))]
    fastest = s.get("sort") == "fastest"
    print("| # | Opening | Est. Value |" + (" Pays In |" if fastest else ""))
    print("|---|---|---|" + ("---|" if fastest else ""))
    for i, r in enumerate(shown, 1):
        est = money(r["value"]) if r["low"] == r["value"] else "{} to {}".format(
            money(r["low"]), money(r["value"]))
        line = "| {} | {} | {} |".format(i, r["name"], est)
        if fastest:
            line += " ~ {} weeks |".format(r["pays_in"])
        print(line)
    print()
    print(json.dumps({"more_at_this_level": len(rows) - len(shown), "held_back": held,
                      "unplaced": unplaced,
                      "numbers": {str(i): r["id"] for i, r in enumerate(shown, 1)}}))


if __name__ == "__main__":
    main()
