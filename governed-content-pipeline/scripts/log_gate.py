#!/usr/bin/env python3
"""Append one gate decision to pipeline/log.jsonl.

    python scripts/log_gate.py --piece kestrel-soc2-linkedin --gate 1 --decision pass \
        --owner "Lena Voss" --reason "7 of 10 supported, 3 cut" \
        --canon security-faq@2.4 --canon customer-proof@1.6 --reuse 0.7

    python scripts/log_gate.py --piece kestrel-soc2-linkedin --gate request --owner "Dana Okafor" --reason "..."
    python scripts/log_gate.py --piece kestrel-soc2-linkedin --gate spot-check --decision pass --owner "Will Kelly" --reason "5/5 trace"

An override without a reason is refused. That's the one rule the script enforces.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", default=Path(__file__).resolve().parent.parent / "pipeline" / "log.jsonl")
    ap.add_argument("--piece", required=True, help="slug")
    ap.add_argument("--gate", required=True, help="0-4, or 'request', or 'spot-check'")
    ap.add_argument("--decision", default=None, help="pass | fail | override (request defaults to 'opened')")
    ap.add_argument("--owner", required=True)
    ap.add_argument("--reason", default="")
    ap.add_argument("--canon", action="append", default=[], help="source id@version, repeatable")
    ap.add_argument("--reuse", type=float, default=None, help="0.0 to 1.0; canon rows / total rows")
    args = ap.parse_args()

    gate = args.gate
    if gate.isdigit():
        gate = int(gate)
        if gate not in range(5):
            sys.exit("gate must be 0-4")
    elif gate not in ("request", "spot-check"):
        sys.exit("gate must be 0-4, 'request', or 'spot-check'")

    decision = args.decision or ("opened" if gate == "request" else None)
    if decision not in ("pass", "fail", "override", "opened"):
        sys.exit("decision must be pass, fail, or override")
    if decision == "override" and not args.reason.strip():
        sys.exit("refused: an override needs a reason. That's the whole point of logging it.")
    if gate == 4 and decision == "override":
        sys.exit("refused: Gate 4 has no override. Someone signs it or it doesn't ship.")

    entry = {
        "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
        "piece": args.piece,
        "gate": gate,
        "decision": decision,
        "owner": args.owner,
        "reason": args.reason,
        "canon_refs": args.canon,
        "reuse": args.reuse,
    }
    with open(args.log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print(json.dumps(entry))


if __name__ == "__main__":
    main()
