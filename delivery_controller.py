# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
delivery_controller.py — Pump Redundancy and VFD Flow Controls
==============================================================
Helix Omega Strand: Practical Delivery & Actuator Controls.
"""
import time

class PumpSystemController:
    def __init__(self, total_pumps: int = 5, min_redundancy: int = 2) -> None:
        self.total_pumps = total_pumps
        self.min_redundancy = min_redundancy
        self.active_pumps = total_pumps - min_redundancy
        self.current_vfd_hz = 50.0

    # 1. PREPARATION LEVEL
    def bootstrap_pumps(self) -> bool:
        print("[COOLING-PREP] Priming fluid pipelines.")
        return True

    # 2. OPERATION LEVEL
    def modulate_flow_by_load(self, system_load_kw: float) -> float:
        # RED TEAM MITIGATION: Dampen VFD acceleration to prevent pressure waves (water hammer)
        target_hz = 50.0
        if system_load_kw > 1000.0:
            target_hz = 60.0
        elif system_load_kw < 400.0:
            target_hz = 35.0
            
        # Limit rate of change to 5.0 Hz per step
        delta = target_hz - self.current_vfd_hz
        if abs(delta) > 5.0:
            self.current_vfd_hz += 5.0 if delta > 0 else -5.0
        else:
            self.current_vfd_hz = target_hz
        return self.current_vfd_hz

    # 3. EMERGENCY REACTION LEVEL
    def handle_pump_failure(self, failed_pump_count: int) -> bool:
        print(f"[COOLING-EMERGENCY] FAILED PUMPS DETECTED: {failed_pump_count}")
        self.active_pumps = max(0, self.active_pumps - failed_pump_count)
        if self.active_pumps < (self.total_pumps - self.min_redundancy):
            print("[COOLING-EMERGENCY] Breached redundancy envelope. Spooling remaining VFDs to max.")
            self.current_vfd_hz = 60.0
            return False
        return True
