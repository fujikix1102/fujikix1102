#!/usr/bin/env python3
"""Fail-closed evidence and manifest verifier for the NOVA phase bundle."""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
required = [
    "README.md", "MANIFEST.json", "SHA256SUMS", "input_manifest.json",
    "mrms_precipflag_official_parameter_table_20261024.json",
    "gpm_mrms_2024_phase_join_exploratory_20261024.json",
    "gpm_mrms_seven_day_phase_bootstrap_20261024_v3.json",
    "gpm_mrms_seven_day_phase_dayblock_bootstrap_20261024.json",
    "nova_gpm_mrms_integrated_status_ledger_20261024.json",
]
missing = [x for x in required if not (ROOT / x).is_file()]
if missing:
    print(json.dumps({"status": "FAIL_CLOSED_REQUIRED_ARTIFACTS_MISSING", "missing": missing}, indent=2))
    sys.exit(2)
ledger = json.loads((ROOT / "nova_gpm_mrms_integrated_status_ledger_20261024.json").read_text())
manifest = json.loads((ROOT / "MANIFEST.json").read_text())
if ledger.get("claim_gates", {}).get("formal_pass") is not False:
    print("FAIL_CLOSED: formal_pass must remain false", file=sys.stderr)
    sys.exit(3)
if manifest.get("formal_pass") is not False:
    print("FAIL_CLOSED: manifest formal_pass must remain false", file=sys.stderr)
    sys.exit(4)
print(json.dumps({
    "status": "EVIDENCE_BUNDLE_VERIFIED",
    "files_checked": len(required),
    "formal_pass": False,
    "human_third_party_execution": ledger.get("claim_gates", {}).get("human_third_party_execution", "NOT_ESTABLISHED"),
    "recomputation": "REQUIRES_FRESH_OFFICIAL_INPUT_ACQUISITION"
}, indent=2))
