#!/usr/bin/env python3
"""Fail-closed validator for a submitted NOVA third-party execution record."""
import hashlib, json, sys
from pathlib import Path

required = ["executor", "environment", "execution_log", "input_sha256", "runner_sha256", "result_sha256"]
if len(sys.argv) != 2:
    print("usage: validate_third_party_evidence.py evidence.json", file=sys.stderr)
    raise SystemExit(2)
p = Path(sys.argv[1])
try:
    d = json.loads(p.read_text())
except Exception as e:
    print(json.dumps({"status":"FAIL_CLOSED_INVALID_JSON", "error":str(e)}))
    raise SystemExit(3)
missing = [k for k in required if not d.get(k)]
serialized = json.dumps(d, ensure_ascii=False)
if "<" in serialized or ">" in serialized:
    missing.append("unreplaced_template_placeholders")
if missing:
    print(json.dumps({"status":"FAIL_CLOSED_REQUIRED_EVIDENCE_MISSING", "missing":missing}, indent=2))
    raise SystemExit(4)
if d.get("human_third_party_execution") != "CONFIRMED_BY_HUMAN_EVIDENCE":
    print(json.dumps({"status":"FAIL_CLOSED_HUMAN_EXECUTION_NOT_CONFIRMED"}, indent=2))
    raise SystemExit(5)
if d.get("formal_pass") is True:
    print(json.dumps({"status":"FAIL_CLOSED_PREMATURE_FORMAL_PASS"}, indent=2))
    raise SystemExit(6)
print(json.dumps({"status":"EVIDENCE_SCHEMA_ACCEPTED_FOR_REVIEW", "formal_pass":False, "sha256":hashlib.sha256(p.read_bytes()).hexdigest()}, indent=2))
