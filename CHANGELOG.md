# Changelog

## v2.0.0 — post-quantum core (2026-10-21)
- **ML-DSA-44 (FIPS 204, NIST)** signature layer: no quantum computer forges a sealed receipt. Public key embedded in the receipt — self-verifying, no server, no CA, no key distribution.
- **Quantum-attested entropy**: receipt ids born from bits measured on real IBM Quantum hardware (job `dbcnmds24mrc73ck0p0g`, ibm_marrakesh, 32 qubits Hadamard, 256 shots, 8192 bits), pool shipped as public beacon in `quantum_entropy_attestation.json`, mixed fresh with OS entropy via SHAKE256.
- SHA3-256 canonical seal kept as layer 1 (Grover-resistant; v1-compatible: old receipts keep verifying).
- CI self-test extended: PQ signature verification in the roundtrip.

## v1.0.0 — initial release
- SHA3-256 canonical seal (Z-QEA).
