#!/usr/bin/env python3
"""Fail-closed public/product truth verification for Cooling Omega."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flow_controller import EVIDENCE_STATE, feedforward_from_requirement, simulate  # noqa: E402

FORBIDDEN_README = (
    "<<<<<<<",
    "=======",
    ">>>>>>>",
    "Automatic failover",
    "Emergency shutdown",
    "Backup cooling",
    "emergency_status",
    "Mastermind alerts",
    "APEX",
    "predictive failure model",
)


def main() -> int:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for token in FORBIDDEN_README:
        if token.lower() in readme.lower():
            raise SystemExit(f"forbidden_public_claim:{token}")

    capabilities = json.loads((ROOT / "machine/capabilities.json").read_text())
    target = json.loads((ROOT / "machine/target-contract.json").read_text())
    excellence = json.loads((ROOT / "machine/excellence-state.json").read_text())
    promotion = json.loads((ROOT / "machine/promotion_authority.json").read_text())
    gaps = json.loads((ROOT / "machine/crystallization/gap-matrix.json").read_text())

    if capabilities["evidence_state"] != EVIDENCE_STATE:
        raise SystemExit("capability_evidence_state_mismatch")
    if target["evidence_state"] != EVIDENCE_STATE:
        raise SystemExit("target_evidence_state_mismatch")
    if excellence["state"] != "FUNCTIONAL_CRYSTALLIZATION_CANDIDATE":
        raise SystemExit("false_terminal_state")
    if promotion["status"] != "RETIRED":
        raise SystemExit("legacy_local_promotion_not_retired")
    if gaps["gaps"] != []:
        raise SystemExit("material_gaps_remain")

    bridge = feedforward_from_requirement(48_000.0, 60_000.0)
    simulation = simulate([40.0, 43.0, 46.0, 44.0, 41.0], feedforward_fraction=bridge["feedforward_fraction"])
    if simulation["outputs"][2] <= simulation["outputs"][0]:
        raise SystemExit("hotter_scenario_did_not_increase_demand")
    if simulation["hardware_actuation"] is not False:
        raise SystemExit("hardware_authority_leak")

    source_sha = hashlib.sha256((ROOT / "src" / "flow_controller.py").read_bytes()).hexdigest()
    receipt = {
        "schema": "glaciereq.cooling-omega.public-proof.v2",
        "evidence_state": EVIDENCE_STATE,
        "source_sha256": source_sha,
        "simulation_digest": simulation["digest"],
        "feedforward_digest": bridge["digest"],
        "external_queries": 0,
        "external_actions": 0,
        "hardware_actuation": False,
        "runtime_pairing_with_alpha": False,
        "legacy_promotion_authority": "RETIRED",
        "result": "PASS",
    }
    out = ROOT / "artifacts" / "public-core" / "verification.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
