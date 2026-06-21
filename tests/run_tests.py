# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
import os
import sys
import time

# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from control_loop import TelemetryLoop
from delivery_controller import PumpSystemController

def test_cooling_control():
    print("[TEST] Running Cooling Control Loop test...")
    t0 = time.perf_counter()
    
    controller = PumpSystemController()
    assert controller.bootstrap_pumps() == True
    
    hz = controller.modulate_flow_by_load(1200.0)
    assert hz == 60.0
    print(f"  - Verified Pump VFD modulation at high load: {hz} Hz")
    
    loop = TelemetryLoop()
    assert loop.initialize_telemetry_links() == True
    
    # Test logging lumping
    for i in range(10):
        loop.run_dynamic_lumped_log(45.0)
    assert loop.nominal_lump_count == 10
    print(f"  - Verified dynamic log lumping. Nominal cycles lumped: {loop.nominal_lump_count}")
    
    # Test predictive warmup
    loop.run_predictive_preactivation("08:50")
    
    duration_ms = (time.perf_counter() - t0) * 1000.0
    print(f"[TEST-METRICS] Status=SUCCESS Latency={duration_ms:.3f}ms")

if __name__ == '__main__':
    test_cooling_control()
