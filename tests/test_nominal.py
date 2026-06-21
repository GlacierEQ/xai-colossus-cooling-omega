# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from delivery_controller import PumpSystemController
def test_nominal():
    ctrl = PumpSystemController()
    hz = ctrl.modulate_flow_by_load(500.0)
    assert hz == 50.0
    print("  [PASS] Nominal delivery controller pump frequency successful.")
