#!/usr/bin/env python3
"""Turn pipeline/log.jsonl into the five numbers from the talk.

    python scripts/metrics.py            # all pieces
    python scripts/metrics.py --since 2026-10-01
    python scripts/metrics.py --json     # machine-readable

The five numbers:
  1. Turnaround time   request -> Gate 4 pass, per shipped piece
  2. Approval latency  time each piece sat waiting at each gate
  3. Gate pass rate    pass / (pass + fail + override), per gate
  4. Reuse rate        ledger rows citing canon / total rows, from Gate 4 entries
  5. Retrieval success spot-check pass rate

No external dependencies. Python 3.9+.
"""

import argparse
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

GATE_NAMES = {0: "Intake", 1: "Sources", 2: "Draft", 3: "Review", 4: "Ship"}


def load(path, since=None):
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                sys.exit(f"{path}:{n}: bad JSON: {e}")
            row["_ts"] = datetime.fromisoformat(row["ts"])
            if since and row["_ts"].date() < since:
                continue
            rows.append(row)
    rows.sort(key=lambda r: r["_ts"])
    return rows


def hours(td):
    return td.total_seconds() / 3600


def fmt_hours(h):
    if h is None:
        return "n/a"
    if h < 48:
        return f"{h:.1f} h"
    return f"{h / 24:.1f} d"


def compute(rows):
    by_piece = defaultdict(list)
    for r in rows:
        by_piece[r["piece"]].append(r)

    # 1. Turnaround: request -> Gate 4 pass
    turnaround = {}
    for piece, evs in by_piece.items():
        opened = next((e for e in evs if e["gate"] == "request"), None)
        shipped = next((e for e in evs if e["gate"] == 4 and e["decision"] == "pass"), None)
        if opened and shipped:
            turnaround[piece] = hours(shipped["_ts"] - opened["_ts"])

    # 2. Approval latency: time from the previous decision (or request) to each gate decision.
    #    A reopened gate counts again; that's the cost of the reopen, and it belongs in the number.
    latency = defaultdict(list)
    for piece, evs in by_piece.items():
        prev = None
        for e in evs:
            if e["gate"] == "spot-check":
                continue
            if prev is not None and isinstance(e["gate"], int):
                latency[e["gate"]].append(hours(e["_ts"] - prev["_ts"]))
            prev = e

    # 3. Gate pass rate
    outcomes = defaultdict(lambda: {"pass": 0, "fail": 0, "override": 0})
    for r in rows:
        if isinstance(r["gate"], int) and r["decision"] in outcomes[r["gate"]]:
            outcomes[r["gate"]][r["decision"]] += 1

    # 4. Reuse rate, from the Gate 4 entry of each shipped piece
    reuse = {}
    for piece, evs in by_piece.items():
        shipped = [e for e in evs if e["gate"] == 4 and e["decision"] == "pass" and e.get("reuse") is not None]
        if shipped:
            reuse[piece] = shipped[-1]["reuse"]

    # 5. Retrieval success
    checks = [r for r in rows if r["gate"] == "spot-check"]
    retrieval = {
        "checked": len(checks),
        "passed": sum(1 for c in checks if c["decision"] == "pass"),
        "failures": [(c["piece"], c["reason"]) for c in checks if c["decision"] != "pass"],
    }

    # Extras the talk cares about: stalled pieces and overrides
    stalled = []
    for piece, evs in by_piece.items():
        if piece not in turnaround:
            gate_events = [e for e in evs if e["gate"] != "spot-check"]
            if not gate_events:
                continue  # only spot-checks in this window; the piece shipped earlier
            last = gate_events[-1]
            stalled.append((piece, last["gate"], last["decision"], last["_ts"].date().isoformat()))
    overrides = [(r["piece"], r["gate"], r["owner"], r["reason"]) for r in rows if r["decision"] == "override"]

    return {
        "pieces": len(by_piece),
        "shipped": len(turnaround),
        "turnaround": turnaround,
        "latency": dict(latency),
        "outcomes": dict(outcomes),
        "reuse": reuse,
        "retrieval": retrieval,
        "stalled": stalled,
        "overrides": overrides,
    }


def report(m):
    out = []
    p = out.append
    p(f"Governed content pipeline: {m['pieces']} pieces in log, {m['shipped']} shipped\n")

    p("1. Turnaround time (request to shipped)")
    if m["turnaround"]:
        vals = list(m["turnaround"].values())
        p(f"   median {fmt_hours(statistics.median(vals))}, min {fmt_hours(min(vals))}, max {fmt_hours(max(vals))}")
        for piece, h in sorted(m["turnaround"].items(), key=lambda kv: kv[1]):
            p(f"   {fmt_hours(h):>8}  {piece}")
    else:
        p("   nothing shipped yet")
    p("")

    p("2. Approval latency (time waiting at each gate, median)")
    for g in sorted(m["latency"]):
        vals = m["latency"][g]
        p(f"   Gate {g} {GATE_NAMES[g]:<8} {fmt_hours(statistics.median(vals)):>8}   (n={len(vals)}, max {fmt_hours(max(vals))})")
    p("")

    p("3. Gate pass rate")
    p("   A gate that never says no can go. A gate that always says no is a Gate 0 problem.")
    for g in sorted(m["outcomes"]):
        o = m["outcomes"][g]
        total = sum(o.values())
        rate = o["pass"] / total if total else 0
        p(f"   Gate {g} {GATE_NAMES[g]:<8} {rate:>5.0%}   pass {o['pass']}, fail {o['fail']}, override {o['override']}")
    p("")

    p("4. Reuse rate (ledger rows pulled from canon, not written fresh)")
    if m["reuse"]:
        p(f"   mean {statistics.mean(m['reuse'].values()):.0%} across shipped pieces")
        for piece, r in m["reuse"].items():
            p(f"   {r:>5.0%}  {piece}")
    p("")

    r = m["retrieval"]
    p("5. Retrieval success (weekly spot-checks: does the shipped claim trace to current canon?)")
    if r["checked"]:
        p(f"   {r['passed']}/{r['checked']} checks passed ({r['passed'] / r['checked']:.0%})")
        for piece, reason in r["failures"]:
            p(f"   FAIL  {piece}: {reason}")
    else:
        p("   no spot-checks logged yet")
    p("")

    if m["overrides"]:
        p(f"Overrides on record: {len(m['overrides'])}")
        for piece, gate, owner, reason in m["overrides"]:
            p(f"   Gate {gate}  {owner:<14} {piece}: {reason}")
        p("")

    if m["stalled"]:
        p("Not shipped")
        for piece, gate, decision, date in m["stalled"]:
            p(f"   {piece}: last seen at Gate {gate} ({decision}) on {date}")
        p("")

    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", default=Path(__file__).resolve().parent.parent / "pipeline" / "log.jsonl")
    ap.add_argument("--since", type=lambda s: datetime.fromisoformat(s).date(), help="YYYY-MM-DD")
    ap.add_argument("--json", action="store_true", help="print the raw numbers as JSON")
    args = ap.parse_args()

    rows = load(args.log, args.since)
    if not rows:
        sys.exit("log is empty")
    m = compute(rows)
    if args.json:
        print(json.dumps(m, indent=2, default=str))
    else:
        print(report(m))


if __name__ == "__main__":
    main()
