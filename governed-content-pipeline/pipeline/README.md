# Pipeline working folders

| Folder | Holds | Written by |
|---|---|---|
| `briefs/` | One brief per piece, `<slug>.md` | `/intake` |
| `ledgers/` | One claims ledger per piece | `/sources` |
| `drafts/` | One draft file per piece, all versions inside | `/draft` |
| `reviews/` | Both auditor reports, check table, fix log | `/review` |
| `shipped/<slug>/` | `final.md`, `ledger.md`, `changelog.md`, `archive-record.yaml` | `/ship` |
| `log.jsonl` | Every gate decision, one JSON line each | `scripts/log_gate.py` |

The folders start empty except for `log.jsonl`, which carries five example pieces so `scripts/metrics.py` has something to report. A finished example of every artifact is in `examples/kestrel-launch-post/`.

Shipped pieces are immutable. If canon changes and a shipped piece is now wrong, that's a new piece that references the old one.
