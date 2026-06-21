# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
control_loop.py — Telemetry Monitoring & Emergency Mitigation Loop
===================================================================
Helix Omega Strand: Async feedback control system monitoring throttling limits.
"""

import asyncio
import logging
from delivery_controller import PumpStation, FlowRegime

log = logging.getLogger("COLOSSUS-OMEGA-LOOP")

class CoolingOrchestrator:
    """Async control loop monitoring GPU thermal thresholds and updating pumps."""
    
    THROTTLE_LIMIT_C = 83.0  # H100/H200 silicon limit
    
    def __init__(self, pump_station: PumpStation) -> None:
        self.pump_station = pump_station
        self.active_loop = True

    async def run_telemetry_loop(self, sensor_api_callback) -> None:
        """Polls sensors and adjustments flow rates dynamically."""
        log.info("Starting Omega telemetry control loop...")
        
        while self.active_loop:
            try:
                gpu_temp = await sensor_api_callback()
                log.info(f"Telemetry update: Peak GPU Silicon Temperature = {gpu_temp}°C")
                
                if gpu_temp >= self.THROTTLE_LIMIT_C:
                    log.warning(f"⚠️ Silicon limits hit ({gpu_temp}°C >= {self.THROTTLE_LIMIT_C}°C)! Executing EMERGENCY_BLAST.")
                    self.pump_station.current_regime = FlowRegime.EMERGENCY_BLAST
                elif gpu_temp >= 75.0:
                    log.info("High load detected. Escalating to SURGE_PREDICTIVE.")
                    self.pump_station.current_regime = FlowRegime.SURGE_PREDICTIVE
                else:
                    self.pump_station.current_regime = FlowRegime.NOMINAL
                    
                actual_lpm = self.pump_station.get_actual_lpm_output()
                log.info(f"Targeting delivery: {actual_lpm:.2f} LPM")
                
            except Exception as e:
                log.error(f"Sensor read exception: {e}")
                
            await asyncio.sleep(0.5)  # 500ms cycle
