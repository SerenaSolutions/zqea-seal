# Z-QEA Receipt Sealer

![seal](https://img.shields.io/badge/seal-SHA3--256-blue) ![license](https://img.shields.io/badge/license-MIT-blue)

**Seal any JSON artifact with a Z-QEA SHA3-256 seal in CI.** The writing counterpart of [Z-QEA Receipt Verifier](https://github.com/marketplace/actions/z-qea-receipt-verifier).

The seal is a public, keyless integrity rule — the receipt declares its own
rule (`selo_regra`), so anyone can recompute and verify: model cards, benchmark
results, experiment records, bill-of-materials, audit evidence — anything that
must arrive *exactly as sealed*.

```yaml
- name: Seal artifact
  uses: SerenaSolutions/zqea-seal@v1
  with:
    file: results.json
    output: results.sealed.json
```

### Inputs / Outputs

| Input | Required | Description |
|-------|----------|-------------|
| `file` | yes | JSON file to seal |
| `output` | no | sealed output path (default `<file>.sealed.json`) |

| Output | Description |
|--------|-------------|
| `seal` | SHA3-256 seal |
| `sealed-file` | path of the sealed file |

Free forever, MIT. ZEPHIRUM product line: [zqea-verify](https://github.com/marketplace/actions/z-qea-receipt-verifier), [zq-gate](https://github.com/SerenaSolutions/zq-gate), [z-anyon-lab](https://github.com/SerenaSolutions/z-anyon-lab).
