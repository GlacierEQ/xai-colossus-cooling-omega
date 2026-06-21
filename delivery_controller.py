# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
delivery_controller.py — Mechanical Flow Control & Pump Redundancy
==================================================================
Helix Omega Strand: Practical delivery systems, flow regimes, and VFD hardware.
"""

from enum import Enum
from dataclasses import dataclass

class FlowRegime(Enum):
    IDLE = 0
    NOMINAL = 1
    SURGE_PREDICTIVE = 2
    EMERGENCY_BLAST = 3
    THERMAL_REBALANCE = 4

class RedundancyPattern(Enum):
    N_PLUS_ONE = 1
    N_PLUS_TWO = 2
    ACTIVE_ACTIVE = 3

@dataclass
class PumpStation:
    station_id: str
    design_flow_lpm: float
    redundancy: RedundancyPattern = RedundancyPattern.N_PLUS_TWO
    active_pumps: int = 4
    backup_pumps: int = 2
    current_regime: FlowRegime = FlowRegime.NOMINAL

    def get_actual_lpm_output(self, efficiency_factor: float = 0.94) -> float:
        """Computes the current delivery LPM based on pump configuration and regime multipliers."""
        base_flow = self.design_flow_lpm * (self.active_pumps / (self.active_pumps + self.backup_pumps))
        
        regime_multipliers = {
            FlowRegime.IDLE: 0.0,
            FlowRegime.NOMINAL: 1.0,
            FlowRegime.SURGE_PREDICTIVE: 1.25,
            FlowRegime.EMERGENCY_BLAST: 1.50,
            FlowRegime.THERMAL_REBALANCE: 1.10
        }
        
        mult = regime_multipliers.get(self.current_regime, 1.0)
        return base_flow * mult * efficiency_factor
