# NOVA GPM–MRMS Phase Reproduction Bundle v1

This bundle contains the updated diagnostic integration for the seven-day GPM–MRMS comparison.

## Contents

- `mrms_precipflag_official_parameter_table_20261024.json`: NOAA/NSSL official PrecipFlag definitions.
- `gpm_mrms_2024_phase_join_exploratory_20261024.*`: 2024-01-07 and 2024-02-01 hourly joins.
- `gpm_mrms_seven_day_phase_bootstrap_20261024_v3.json`: seven-day hourly phase-stratified bootstrap.
- `gpm_mrms_seven_day_phase_dayblock_bootstrap_20261024.json`: day-block bootstrap and LODO audit.
- `nova_gpm_mrms_integrated_status_ledger_20261024.json`: evidence and claim-status ledger.
- `input_manifest.json`: fresh official-acquisition contract.
- `verify_bundle.py`: fail-closed evidence verifier.
- `verifier_fault_injection_20261024.json`: negative tests for fail-closed behavior.

## Reproduction boundary

This is a diagnostic comparison bundle. It does not contain a physical precipitation truth, a calibration coefficient, or human third-party execution evidence. `formal_pass` is intentionally `false`.

The 2024 phase assignment uses the official flag table and the dominant class among 29 basin cells. Ties and missing/out-of-coverage values are not silently converted into rain or snow.

## Reproduction

1. Verify `SHA256SUMS`.
2. Read the official mapping artifact.
3. Join hourly GPM–MRMS rows by exact UTC hour.
4. Recompute hourly phase summaries and day-block bootstrap with the declared seed and 10,000 replicates.
5. Confirm that no claim is promoted beyond the statuses in the integrated ledger.

Run `python3 verify_bundle.py` for the local evidence gate. This verifies the included evidence package; it does not download or recompute raw GPM/MRMS data.
