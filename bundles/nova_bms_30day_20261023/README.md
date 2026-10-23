# NOVA BMS 30-day third-party reproduction bundle

This is the public, text-only evidence package for the SRRL BMS June 2023 comparison of Global CMP22 (vent/cor) [W/m^2], Kipp & Zonen CMP22, serial 080017.

## Status
- external reproduction: EXTERNAL_REPRODUCTION_PENDING
- human third-party execution: NOT_ESTABLISHED
- formal_pass: false

## Included
The JSON files are provenance, integration, and value-fixed-workbook manifests.
The 30 daily Excel workbooks are not included in this GitHub Contents package: the local workbook set is approximately 69 MB and must be transferred as a separate shareable archive or release asset before a third party can reproduce the workbook calculation itself. The manifest records the expected workbook names and hashes.

## Reproduction requirements
1. Use the source workbooks without modifying the originals.
2. Recalculate and save Calculation_final X/Y values for all 30 days.
3. Verify 3,911 rows per day and report formula/error cells.
4. Report input, spreadsheet-engine/environment, runner, and result SHA-256 values.
5. Keep BORCAL calibration uncertainty separate from workbook-derived field uncertainty.
6. Do not promote this bundle to formal validation or a calibration correction.

## Evidence requested on Issue #2
Attach the execution log, environment and spreadsheet-engine details, input SHA-256, runner SHA-256, result SHA-256, and final error count.

Issue: https://github.com/fujikix1102/fujikix1102/issues/2