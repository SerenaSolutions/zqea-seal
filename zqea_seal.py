#!/usr/bin/env python3
"""Z-QEA Receipt Sealer — seal a JSON artifact with a Z-QEA SHA3-256 seal.

Canonical rule (declared, public, no key):
  selo = SHA3-256 over json.dumps(payload, sort_keys=True, ensure_ascii=True,
  default=str) with the field selo_sha3_256 REMOVED from the input.
The receipt also declares its own rule in selo_regra — verification needs no
server and no key: recompute and compare (see SerenaSolutions/zqea-verify).

Usage: python3 zqea_seal.py input.json [-o sealed.json]
Exit 0 = sealed; 2 = usage/malformed.
"""
import sys, os, json, argparse, hashlib

def seal(rec):
    payload = {k: v for k, v in rec.items() if k != "selo_sha3_256"}
    return hashlib.sha3_256(json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode()).hexdigest()

RULE = "selo = SHA3-256 sobre json.dumps(recibo, sort_keys=True, ensure_ascii=True, default=str) com o campo selo_sha3_256 REMOVIDO da entrada"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="JSON file to seal")
    ap.add_argument("-o", "--output", help="sealed output path (default: <input>.sealed.json)")
    a = ap.parse_args()
    try:
        rec = json.load(open(a.input))
    except Exception as e:
        print("Z-QEA SEAL: MALFORMED INPUT —", e); return 2
    if not isinstance(rec, dict):
        print("Z-QEA SEAL: top-level JSON must be an object"); return 2
    rec["selo_regra"] = RULE
    rec["selo_sha3_256"] = seal(rec)
    out = a.output or (a.input.rsplit(".json", 1)[0] + ".sealed.json")
    json.dump(rec, open(out, "w"), ensure_ascii=True, indent=1)
    print("Z-QEA: SEALED ->", out, "| selo:", rec["selo_sha3_256"])
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("seal=" + rec["selo_sha3_256"] + "\n")
            f.write("sealed-file=" + out + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
