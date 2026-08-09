#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flow_controller import control_loop  # noqa: E402


def sha256_json(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    test = subprocess.run(
        [sys.executable, "tests/test_flow_controller.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if test.returncode != 0:
        raise SystemExit(test.stderr or test.stdout or "flow-controller test failed")

    scenario = control_loop([40.0, 50.0, 70.0, 85.0])
    flows = scenario["flows"]
    if not flows or any(not 0.0 <= value <= 1.0 for value in flows):
        raise SystemExit("modeled flow decisions escaped the declared 0..1 boundary")

    receipt = {
        "schema": "glaciereq.cooling-omega.public-proof.v1",
        "capability": "modeled_flow_control_policy",
        "evidence_level": "TEST",
        "scenario": scenario,
        "external_queries": 0,
        "external_actions": 0,
        "live_telemetry": False,
        "hardware_actuation": False,
        "runtime_pairing_with_alpha": False,
        "test_returncode": test.returncode,
    }
    receipt["receipt_sha256"] = sha256_json(receipt)
    out = ROOT / "artifacts" / "public-core"
    out.mkdir(parents=True, exist_ok=True)
    (out / "verification.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
