// ============================================================================
// Z-QEA RECEIPT SEALER — demo artifact circuit in OpenQASM 3
// The measured results of this circuit are the JSON artifact that the CI
// self-test seals with a Z-QEA SHA3-256 seal (quantum/measure_demo.json).
// Seal = SHA3-256 over canonical JSON, keyless, declared in the receipt itself.
// ============================================================================
OPENQASM 3.0;
include "stdgates.inc";

// Grover on 2 qubits: target |11>, one iteration — p(|11>) = 1.0 exactly
qubit[2] grover;
bit[2] measured;
reset grover;
h grover[0];
h grover[1];
cz grover[0], grover[1];                 // oracle: mark |11>
h grover[0]; h grover[1];
x grover[0]; x grover[1];
cz grover[0], grover[1];                 // diffuser
x grover[0]; x grover[1];
h grover[0]; h grover[1];
measure grover -> measured;

// ---------------------------------------------------------------------------
// Demo artifact 2 — Deutsch-Jozsa n=2, balanced oracle: trivalent REFUSED
// ---------------------------------------------------------------------------
qubit[3] dj;
bit[2] dj_out;
reset dj;
x dj[2];
h dj[2];
h dj[0]; h dj[1];
cx dj[0], dj[2];
cx dj[1], dj[2];
h dj[0]; h dj[1];
measure dj[0:2] -> dj_out;

// ---------------------------------------------------------------------------
// Demo artifact 3 — Bell pair: parity correlation (|00> + |11>)/sqrt(2)
// Sealing the measured artifact proves the measurement record arrived intact.
// ---------------------------------------------------------------------------
qubit[2] bell;
bit[2] bell_out;
reset bell;
h bell[0];
cx bell[0], bell[1];
measure bell -> bell_out;
