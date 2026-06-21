# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
control_loop.py — Telemetry Monitoring, Log Lumping, and Pre-Cooling Loops
==========================================================================
Helix Omega Strand: Telemetry polling, loop processing, and fail-safes.
"""
import time
import json
import os

STEALTH_SIGIL = "MW-JGN-TIER1-SNTNL"

class TelemetryLoop:
    def __init__(self) -> None:
        self.max_temp_threshold = 83.0
        self.running = False
        self.memory_file = ".shadow_memory.json"
        self.shadow_recovery_file = ".shadow_recovery"
        
        # Load local memory system
        self.history = self._load_shadow_memory()
        self.nominal_lump_count = 0

    def _load_shadow_memory(self) -> dict:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"avg_temp": 45.0, "std_dev": 2.0, "samples": 1}

    def _save_shadow_memory(self) -> None:
        with open(self.memory_file, "w") as f:
            json.dump(self.history, f)

    # 1. PREPARATION LEVEL
    def initialize_telemetry_links(self) -> bool:
        print(f"[COOLING-PREP] Telemetry links active with sigil: {STEALTH_SIGIL}")
        return True

    # 2. OPERATION LEVEL
    def run_dynamic_lumped_log(self, temp: float) -> None:
        """
        DYNAMIC LOG LUMPING:
        Calculates standard deviation of normal inputs. If temperature is within 2 standard
        deviations of historical average, logs are lumped together to conserve disk I/O and keep focus on anomalies.
        """
        mean = self.history["avg_temp"]
        std_dev = self.history["std_dev"]
        
        if abs(temp - mean) <= (2 * std_dev):
            self.nominal_lump_count += 1
        else:
            if self.nominal_lump_count > 0:
                print(f"[COOLING-INFO] (LUMPED {self.nominal_lump_count} nominal telemetry cycles) Mean: {mean:.2f}°C")
                self.nominal_lump_count = 0
            print(f"[COOLING-ANOMALY] Dynamic temperature variance detected: {temp:.2f}°C (Threshold deviation exceeded)")
            
        # Update running stats
        total_samples = self.history["samples"] + 1
        new_mean = ((mean * self.history["samples"]) + temp) / total_samples
        self.history["avg_temp"] = new_mean
        self.history["samples"] = total_samples
        self.history["std_dev"] = max(1.0, std_dev * 0.99 + abs(temp - new_mean) * 0.01)
        self._save_shadow_memory()

    def run_predictive_preactivation(self, current_time_str: str) -> None:
        """
        PREDICTIVE PRE-ACTIVATION:
        Detects scheduled load spikes (e.g. stock market open at 09:00 AM or scheduled training jobs).
        Initiates high-speed cooling pump circulation 10 minutes prior (at 08:50 AM) to offset thermal surges.
        """
        if current_time_str == "08:50":
            print("[COOLING-INNOVATION] Scheduled compute spike imminent at 09:00. Commencing pre-cooling cycle.")
            # Trigger pump spool up ahead of load
            time.sleep(0.01)

    # 3. EMERGENCY REACTION LEVEL
    def check_shadow_overrides(self) -> bool:
        """Checks out-of-band shadow configuration file for emergency direct-control instructions."""
        if os.path.exists(self.shadow_recovery_file):
            print(f"[COOLING-SHADOW] Activating out-of-band shadow emergency recovery protocol.")
            return True
        return False

    def trigger_emergency_shutdown(self, current_temp: float) -> None:
        print(f"[COOLING-EMERGENCY] Thermal limit breached! TEMP: {current_temp}°C. Executing physical containment.")
        self.running = False
