# NOVA BMS CMP22 v7 — independent execution checklist

## 1. Obtain and verify the archive

Download the v7 archive from the public Issue #2 link and verify:

```text
SHA-256 = 866b49e4b82139633e956890cae7c1aa645ab19bddfb4de059be9428e88e6781
```

After extraction, verify every entry in `SHA256SUMS` before running any analysis.

## 2. Record the environment

Report the operating system, Python version, spreadsheet engine if used, and dependency versions. Do not use the original local filesystem paths.

## 3. Re-acquire official inputs

Use `bms-cmp22-v6-input-manifest.json`. Record the downloaded input SHA-256 values and stop if the official response structure, row count, timezone, or required variables differ.

## 4. Run the portable checker and runner

Use explicit input and output paths. Preserve the stdout/stderr log and the resulting JSON SHA-256.

## 5. Submit evidence to Issue #2

Report:

- executor identity or organization;
- environment and dependency versions;
- input SHA-256 values;
- runner/checker SHA-256 values;
- result SHA-256;
- row counts and gate results;
- manual interventions and deviations.

An automated workflow or a self-run by the bundle author does not establish human third-party execution. Until an independent human submits the evidence above, keep `human_third_party_execution=NOT_ESTABLISHED`, `external_verified=false`, and `formal_pass=false`.
