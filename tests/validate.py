"""Consistency checks for formats.json (Python 3 standard library only).

Run: python tests/validate.py
Checks that every example is well formed and internally consistent: a buy has its
stop-loss below and its targets above the entry, a sell the other way round.
Exit code 0 = all checks passed, 1 = at least one failure.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "formats.json"), encoding="utf-8"))
INTENTS = {"ENTRY", "RESULT", "MANAGEMENT", "NONE"}
failures = []


def check(ok, msg):
    if not ok:
        failures.append(msg)


ids = [f["id"] for f in data["formats"]]
check(len(ids) == len(set(ids)), "duplicate ids")
for f in data["formats"]:
    fid, e = f["id"], f["expect"]
    check(f["market"] in ("forex", "crypto"), "%s: market must be forex or crypto" % fid)
    check(isinstance(f["text"], str) and f["text"].strip(), "%s: empty text" % fid)
    is_entry = f["market"] == "crypto" or e.get("intent") == "ENTRY"
    if f["market"] == "forex":
        check(e.get("intent") in INTENTS, "%s: unknown intent" % fid)
    if not is_entry:
        check(set(e) == {"intent"}, "%s: a non-entry example only states its intent" % fid)
        continue
    check(e.get("symbol") and e["symbol"].upper() == e["symbol"], "%s: symbol must be upper case" % fid)
    check(e.get("side") in ("buy", "sell"), "%s: side must be buy or sell" % fid)
    ref = e.get("entry")
    if e.get("entry_range"):
        lo, hi = e["entry_range"]
        check(lo <= hi, "%s: entry_range must be [low, high]" % fid)
        ref = ref if ref is not None else (lo + hi) / 2
    sign = 1 if e["side"] == "buy" else -1
    if ref is not None and e.get("sl") is not None:
        check(sign * (ref - e["sl"]) > 0, "%s: stop-loss is on the wrong side of the entry" % fid)
    for tp in e.get("tp_list", []):
        if ref is not None:
            check(sign * (tp - ref) > 0, "%s: target %s is on the wrong side of the entry" % (fid, tp))
    tps = e.get("tp_list", [])
    check(tps == sorted(tps, reverse=(sign < 0)), "%s: targets are not in order" % fid)

if failures:
    print("FAILED")
    for m in failures:
        print(" -", m)
    sys.exit(1)
print("OK: %d examples checked" % len(data["formats"]))
