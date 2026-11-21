#!/usr/bin/env python3
"""Check a proposal's pricing and milestones, and print the venue's fields.

Usage:  python3 proposal_terms.py terms.json      (or JSON on stdin)

Input:
  {"pricing": [{"item": ..., "quantity": 1, "unit_price": 1500}, ...],
   "discount": 0,
   "milestones": [{"description": ..., "amount": 750, "due_date": "2026-12-04"}, ...]}

  pricing      the line items of the proposal's pricing table
  discount     an amount the owner chose to take off; omit for none
  milestones   what is delivered and paid at each step. due_date is required,
               as YYYY-MM-DD.
  today        the date, as YYYY-MM-DD; omit to use the machine's date

It fails, naming the fault, when: a milestone's description is over 200
characters; a milestone's amount is under $5 or over $50,000; a milestone has
no due date, or one that is not a date, is before today, or is not later than
the milestone before it; the milestones do not add up to the pricing total; or
there is no milestone.

On success it prints the pricing table, the milestone table, and one line of
JSON holding the fields the venue takes: charged_amount, payment_mode and
milestones. Pass those to the venue unchanged.
"""
import json
import sys
from datetime import date


def main():
    src = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    d = json.load(src)
    faults = []
    lines = [(i["item"], i.get("quantity", 1), float(i["unit_price"])) for i in d["pricing"]]
    subtotal = sum(q * p for _, q, p in lines)
    discount = float(d.get("discount") or 0)
    total = subtotal - discount
    stones = d.get("milestones") or []
    if not stones:
        faults.append("there is no milestone")
    last = date.fromisoformat(d["today"]) if d.get("today") else date.today()
    for n, m in enumerate(stones, 1):
        try:
            due = date.fromisoformat(str(m.get("due_date") or ""))
        except ValueError:
            faults.append("milestone {} has no due date; give one as YYYY-MM-DD".format(n))
        else:
            if due < last or (n > 1 and due == last):
                faults.append("milestone {} is due {}, which is {}".format(
                    n, due, "before today" if n == 1 else "not after milestone {}".format(n - 1)))
            last = max(last, due)
        if len(m["description"]) > 200:
            faults.append("milestone {} is {} characters; the venue takes 200".format(
                n, len(m["description"])))
        if not 5 <= float(m["amount"]) <= 50000:
            faults.append("milestone {} is outside $5 to $50,000".format(n))
    paid = sum(float(m["amount"]) for m in stones)
    if stones and abs(paid - total) > 0.005:
        faults.append("the milestones add up to ${:,.2f} and the pricing to ${:,.2f}".format(paid, total))
    if faults:
        print("Not ready: " + "; ".join(faults) + ".")
        sys.exit(1)
    print("| Item | Quantity | Unit price | Amount |")
    print("|---|---|---|---|")
    for item, q, p in lines:
        print("| {} | {:g} | ${:,.2f} | ${:,.2f} |".format(item, q, p, q * p))
    if discount:
        print("| Subtotal | | | ${:,.2f} |".format(subtotal))
        print("| Discount | | | -${:,.2f} |".format(discount))
    print("| **Total** | | | **${:,.2f}** |".format(total))
    print()
    print("| # | You receive | Due | Payment |")
    print("|---|---|---|---|")
    for n, m in enumerate(stones, 1):
        print("| {} | {} | {} | ${:,.2f} |".format(n, m["description"], m["due_date"], float(m["amount"])))
    print()
    venue = [{"description": m["description"], "amount": float(m["amount"]), "due_date": m["due_date"]}
             for m in stones]
    print(json.dumps({"charged_amount": total, "payment_mode": "by_milestone", "milestones": venue}))


if __name__ == "__main__":
    main()
