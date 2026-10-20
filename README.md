# NOVA

**NOVA** is an auditable, cross-domain scientific computing framework for reproducibility, uncertainty analysis, and evidence-based validation.

## Purpose

NOVA compares numerical methods across scientific domains and tests whether methods can be transferred safely between problems with compatible mathematical and physical structure.

## Validation model

- Input, runner, solver, validation, calibration, and external-reproduction evidence are kept separate.
- File provenance, execution environment, outputs, and evidence are recorded with SHA-256 manifests.
- Missing data, calibration, or independent reproduction stops promotion rather than being silently inferred.
- formal_pass=false is retained unless the required evidence is actually established.

## Public re-execution projects

- [GW re-execution](https://github.com/fujikix1102/nova-gw-reexecution-20261002)
- [SCEDC re-execution](https://github.com/fujikix1102/nova-scedc-fixed-reexecution-20261002)
- [Temperature re-execution](https://github.com/fujikix1102/nova-public-temperature-reexecution-20261001)
- [Rainfall and wind re-execution](https://github.com/fujikix1102/nova-hagibis-rainfall-wind-reexecution-20261002)

## Evidence levels

- CONTRACT_VERIFIED: input/output contract and failure gates verified.
- BENCHMARK_VERIFIED: public benchmark or synthetic reference verified.
- REAL_DATA_VERIFIED: real-data solver path verified for the stated scope.
- PHYSICAL_CALIBRATION_VERIFIED: external calibration evidence is linked to the measurement.

Independent third-party execution and external calibration remain separate requirements. NOVA does not claim scientific discovery or physical certification from an internal run alone.

## Contact

Junichi Fujiki — independent researcher, Osaka, Japan.
