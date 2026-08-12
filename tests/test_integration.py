from __future__ import annotations

import json
import subprocess
import sys


def test_direct_operator_exercises_requirement_bridge_and_policy() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/operate.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    receipt = json.loads(result.stdout)
    assert receipt["result"] == "PASS"
    assert receipt["feedforward_bridge"]["feedforward_fraction"] == 0.8
    assert receipt["scenario"]["hardware_actuation"] is False
