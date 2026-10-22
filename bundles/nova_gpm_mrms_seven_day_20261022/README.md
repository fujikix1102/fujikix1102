# NOVA GPM–MRMS seven-day reproduction bundle

This bundle is diagnostic only. It does not establish calibration, a universal product correction, or formal validation.

## Reproduction

1. Obtain the raw GPM files and raw MRMS files listed by the input manifests.
2. Verify every raw-file SHA-256 before execution.
3. Install Python dependencies: `h5py numpy xarray cfgrib shapely`.
4. Run the runner scripts in `runner/` with the paths adjusted to the local raw-data directories.
5. Compare regenerated JSON and SHA-256 with `results/`.

Human third-party execution remains `NOT_ESTABLISHED` until an independent person submits execution logs and input/runner/result SHA-256 values.
