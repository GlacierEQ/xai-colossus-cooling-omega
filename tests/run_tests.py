# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
import os
import sys
import time

def run_all_tests():
    print(f"\n=== Running Multi-file Test Suite for: {os.path.basename(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))} ===")
    t_start = time.perf_counter()
    
    # Clean previous shadow memory cache
    shadow_mem = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".shadow_memory.json"))
    if os.path.exists(shadow_mem):
        os.remove(shadow_mem)
        
    # Clear previous overrides
    shadow_rec = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".shadow_recovery"))
    if os.path.exists(shadow_rec):
        os.remove(shadow_rec)
        
    # Import and run each test module
    from test_nominal import test_nominal
    from test_emergency import test_emergency
    from test_compaction import test_compaction
    from test_integration import test_integration
    
    try:
        test_nominal()
        test_emergency()
        test_compaction()
        test_integration()
    except Exception as e:
        print(f"  [FAIL] Test execution encountered error: {e}")
        sys.exit(1)
        
    duration_ms = (time.perf_counter() - t_start) * 1000.0
    print(f"[TEST-METRICS] Status=SUCCESS Latency={duration_ms:.3f}ms")
    sys.exit(0)

if __name__ == '__main__':
    run_all_tests()
