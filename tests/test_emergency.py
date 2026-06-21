# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from delivery_controller import PumpSystemController
from control_loop import TelemetryLoop
def test_emergency():
    ctrl = PumpSystemController()
    assert ctrl.handle_pump_failure(3) == False
    loop = TelemetryLoop()
    loop.initialize_telemetry_links()
    loop.trigger_emergency_shutdown(85.0)
    assert loop.running == False
    print("  [PASS] Emergency pump backup spools and shutdown loops validated.")
