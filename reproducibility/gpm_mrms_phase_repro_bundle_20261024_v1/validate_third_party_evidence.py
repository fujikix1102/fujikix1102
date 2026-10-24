#!/usr/bin/env python3
"""Fail-closed validator for a submitted NOVA third-party execution record."""
import hashlib, json, sys
from pathlib import Path

REQUIRED = ["executor", "environment", "execution_log", "input_sha256", "runner_sha256", "result_sha256"]

if len(sys.argv) != 2:
    print("usage: validate_third_party_evidence.py evidence.json", file=sys.stderr)
    raise SystemExit(2)
path = Path(sys.argv[1])
try:
    record = json.loads(path.read_text())
except Exception as exc:
    print(json.dumps({"status": "FAIL_CLOSED_INVALID_JSON", "error": str(exc)}))
    raise SystemExit(3)
missing = [key for key in REQUIRED if not record.get(key)]
if missing:
    print(json.dumps({"status": "FAIL_CLOSED_REQUIRED_EVIDENCE_MISSING", "missing": missing}, indent=2))
    raise SystemExit(4)
if record.get("human_third_party_execution") != "CONFIRMED_BY_HUMAN_EVIDENCE":
    print(json.dumps({"status": "FAIL_CLOSED_HUMAN_EXECUTION_NOT_CONFIRMED"}, indent=2))
    raise SystemExit(5)
if record.get("formal_pass") is True:
    print(json.dumps({"status": "FAIL_CLOSED_PREMATURE_FORMAL_PASS"}, indent=2))
    raise SystemExit(6)
print(json.dumps({"status": "EVIDENCE_SCHEMA_ACCEPTED_FOR_REVIEW", "formal_pass": False,
                  "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, indent=2))
