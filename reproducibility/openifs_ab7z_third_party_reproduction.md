# OpenIFS 48R1 ab7z third-party reproduction procedure

This procedure is for an independent human-controlled reproduction of the ECMWF OpenIFS 48R1 Karl case.

## Fixed reference

- Source branch: `openifs-lts/CY48R1.1`
- Source commit: `3fd8ebe2239ed76d70dc1ac11e13ba01ba8a1e9f`
- Case: `ab7z`, initial date `2016092500`, T159/N80
- Official case archive: https://openifs.ecmwf.int/data/experiments/2016-09_Karl/48r1/ab7z.tar.gz
- Official run documentation: https://github.com/ecmwf-ifs/openifs/blob/openifs-lts/CY48R1.1/docs/oifs_howto_run_experiments.md

## Required execution

Use the unmodified official case archive and record its SHA-256 before extraction.

Build `ifsMASTER.DP` from the fixed source commit using the platform's documented compiler, MPI, NetCDF, HDF5, and ecCodes dependencies. Record compiler, MPI, OS, CPU architecture, and binary SHA-256.

In the extracted case directory `ab7z/2016092500`, use:

- `OIFS_EXPID=ab7z`
- `OIFS_RES=159`
- `OIFS_GRIDTYPE=l`
- `OIFS_NPROC=4`
- `OIFS_NTHREAD=1`
- `CSTOP=h144`

Run the official `scripts/exp_3d/oifs-run` workflow with an explicit four-rank MPI launcher. Do not edit initial GRIB files, static data, or the case namelist except for documented platform configuration. Record every command and exit code.

## Required evidence

Submit:

1. executor identity and independent environment;
2. OS, CPU, compiler, MPI, NetCDF/HDF5/ecCodes versions;
3. source commit;
4. input archive and static-data SHA-256 values;
5. runner/binary SHA-256;
6. full execution log;
7. exit code and maximum forecast step;
8. output file list, sizes, and SHA-256 values;
9. GRIB readability/count checks;
10. differences from the published audit, if any.

The local reference run completed 144/144 hours with exit code 0 and 57 postprocessed output files. This reference is not third-party evidence.

## Status boundary

Download-only verification, GitHub Actions, or replay performed by the requester does not establish human third-party execution.

```
human_third_party_execution=NOT_ESTABLISHED
external_verified=false
formal_pass=false
```
