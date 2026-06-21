# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from control_loop import TelemetryLoop
def test_compaction():
    loop = TelemetryLoop()
    for _ in range(5):
        loop.run_dynamic_lumped_log(45.0)
    assert loop.nominal_lump_count == 5
    print("  [PASS] Log compaction: 5 nominal cycles lumped successfully.")
