#!/usr/bin/env python3
"""Z-QEA Receipt Sealer v2.0.0 — post-quantum sealed receipts.

v2 core (two layers, one receipt):
  1. selo_sha3_256 — SHA3-256 canonical seal (Grover-resistant, same rule
     since v1: old receipts keep verifying, old verifiers keep passing).
  2. assinatura_pq — ML-DSA-44 (FIPS 204): post-quantum signature with the
     public key EMBEDDED in the receipt. Self-verifying: no server, no CA,
     no key distribution. No quantum computer forges this receipt.
  3. receipt id born from QUANTUM entropy: bits measured on real IBM Quantum
     hardware (attested pool, see quantum_entropy_attestation.json) mixed
     with fresh OS entropy via SHAKE256.

Usage: python3 zqea_seal.py input.json [-o sealed.json]
Exit 0 = sealed; 2 = usage/malformed.
"""
import sys, os, json, argparse, hashlib
from zqea_pq import (quantum_receipt_id, entropy_provenance,
                    sign_receipt, sha3_seal, canonical)

RULE = "selo = SHA3-256 sobre json.dumps(recibo, sort_keys=True, ensure_ascii=True, default=str) com o campo selo_sha3_256 REMOVIDO da entrada"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="JSON file to seal")
    ap.add_argument("-o", "--output", help="sealed output path (default: <input>.sealed.json)")
    ap.add_argument("--chain", metavar="PREV_RECEIPT",
                    help="v2.1.0 — cadeia de proveniencia: sela o selo SHA3-256 do recibo anterior")
    a = ap.parse_args()
    try:
        rec = json.load(open(a.input))
    except Exception as e:
        print("Z-QEA SEAL: MALFORMED INPUT —", e); return 2
    if not isinstance(rec, dict):
        print("Z-QEA SEAL: top-level JSON must be an object"); return 2
    if a.chain:
        try:
            prev = json.load(open(a.chain))
            prev_selo = prev.get("selo_sha3_256")
            if not prev_selo:
                print("Z-QEA SEAL: recibo anterior sem selo_sha3_256 — cadeia recusada"); return 2
            rec["previous_seal"] = prev_selo
            rec["previous_receipt"] = os.path.basename(a.chain)
        except Exception as e:
            print("Z-QEA SEAL: nao foi possivel ler o recibo anterior —", e); return 2
    rec["selo_regra"] = RULE
    rec["recibo_id"] = quantum_receipt_id("zqea-seal")
    rec["entropia_quantica"] = entropy_provenance()
    # layer 2: post-quantum signature (pk embedded, self-verifying)
    rec = sign_receipt(rec)
    # layer 1: SHA3-256 canonical seal over everything except the seal itself
    payload = {k: v for k, v in rec.items() if k != "selo_sha3_256"}
    rec["selo_sha3_256"] = sha3_seal(payload)
    out = a.output or (a.input.rsplit(".json", 1)[0] + ".sealed.json")
    json.dump(rec, open(out, "w"), ensure_ascii=True, indent=1)
    print("Z-QEA v2: SEALED ->", out)
    print("  selo SHA3-256   :", rec["selo_sha3_256"])
    print("  assinatura PQ    :", rec["assinatura_pq"]["alg"])
    print("  entropia quantica: job", rec["entropia_quantica"].get("job_id"), "(", rec["entropia_quantica"].get("backend"), ")")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("seal=" + rec["selo_sha3_256"] + "\n")
            f.write("receipt-id=" + rec["recibo_id"] + "\n")
            f.write("sealed-file=" + out + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
