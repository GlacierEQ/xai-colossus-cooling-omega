#!/usr/bin/env python3
"""Execute Cooling Omega's actual stateful response policy directly."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flow_controller import EVIDENCE_STATE, feedforward_from_requirement, simulate  # noqa: E402


def main() -> int:
    bridge = feedforward_from_requirement(48_000.0, 60_000.0)
    scenario = simulate(
        [40.0, 43.0, 46.0, 44.0, 41.0],
        feedforward_fraction=bridge["feedforward_fraction"],
    )
    hot_output = scenario["outputs"][2]
    cold_output = scenario["outputs"][0]
    receipt = {
        "schema": "glaciereq.cooling-omega.operability.v1",
        "evidence_state": EVIDENCE_STATE,
        "feedforward_bridge": bridge,
        "scenario": scenario,
        "result": "PASS" if hot_output > cold_output and scenario["hardware_actuation"] is False else "FAIL",
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
