#!/usr/bin/env python3
"""Bounded stateful thermal-response policy for local simulation.

Outputs are normalized modeled demand fractions only. No telemetry is read and
no hardware or external system is mutated.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Iterable, Any

EVIDENCE_STATE = "LOCAL_STATEFUL_COOLING_RESPONSE_POLICY_NOT_XAI_HARDWARE_CONTROL"
TARGET_C = 42.0


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_must_be_number")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name}_must_be_finite")
    return value


def _clamp(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def _digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PolicyConfig:
    target_c: float = TARGET_C
    kp: float = 0.08
    ki: float = 0.02
    kd: float = 0.01
    integral_limit: float = 10.0
    output_min: float = 0.0
    output_max: float = 1.0

    def validated(self) -> "PolicyConfig":
        values = {
            "target_c": self.target_c,
            "kp": self.kp,
            "ki": self.ki,
            "kd": self.kd,
            "integral_limit": self.integral_limit,
            "output_min": self.output_min,
            "output_max": self.output_max,
        }
        for name, value in values.items():
            _finite(name, value)
        if self.kp < 0 or self.ki < 0 or self.kd < 0:
            raise ValueError("gains_must_be_non_negative")
        if self.integral_limit <= 0:
            raise ValueError("integral_limit_must_be_positive")
        if self.output_min < 0 or self.output_max > 1 or self.output_min >= self.output_max:
            raise ValueError("output_bounds_must_be_ordered_within_zero_one")
        return self


class ResponsePolicy:
    def __init__(self, config: PolicyConfig | None = None):
        self.config = (config or PolicyConfig()).validated()
        self._integral = 0.0
        self._prev_error: float | None = None
        self._step_index = 0

    def reset(self) -> None:
        self._integral = 0.0
        self._prev_error = None
        self._step_index = 0

    def state(self) -> dict[str, Any]:
        return {
            "integral": round(self._integral, 9),
            "previous_error_c": None if self._prev_error is None else round(self._prev_error, 9),
            "step_index": self._step_index,
        }

    def step(
        self,
        temperature_c: float,
        dt: float = 1.0,
        feedforward_fraction: float = 0.0,
    ) -> dict[str, Any]:
        temp = _finite("temperature_c", temperature_c)
        delta_t = _finite("dt", dt)
        feedforward = _finite("feedforward_fraction", feedforward_fraction)
        if delta_t <= 0:
            raise ValueError("dt_must_be_positive")
        if not 0.0 <= feedforward <= 1.0:
            raise ValueError("feedforward_fraction_must_be_between_zero_and_one")

        cfg = self.config
        error = temp - cfg.target_c
        proportional = cfg.kp * error
        next_integral = _clamp(
            self._integral + error * delta_t,
            -cfg.integral_limit,
            cfg.integral_limit,
        )
        integral_term = cfg.ki * next_integral
        derivative_error = 0.0 if self._prev_error is None else (error - self._prev_error) / delta_t
        derivative_term = cfg.kd * derivative_error
        raw = feedforward + proportional + integral_term + derivative_term
        output = _clamp(raw, cfg.output_min, cfg.output_max)

        reasons: list[str] = []
        if error > 0:
            reasons.append("ABOVE_TARGET")
        elif error < 0:
            reasons.append("BELOW_TARGET")
        else:
            reasons.append("AT_TARGET")
        if output >= cfg.output_max and raw > cfg.output_max:
            reasons.append("SATURATED_HIGH")
        if output <= cfg.output_min and raw < cfg.output_min:
            reasons.append("SATURATED_LOW")
        if abs(next_integral) >= cfg.integral_limit and abs(self._integral + error * delta_t) > cfg.integral_limit:
            reasons.append("INTEGRAL_CLAMPED")

        self._integral = next_integral
        self._prev_error = error
        self._step_index += 1

        receipt: dict[str, Any] = {
            "schema": "glaciereq.cooling-omega.policy-step.v1",
            "evidence_state": EVIDENCE_STATE,
            "step_index": self._step_index,
            "temperature_c": round(temp, 9),
            "target_c": round(cfg.target_c, 9),
            "dt": round(delta_t, 9),
            "error_c": round(error, 9),
            "feedforward_fraction": round(feedforward, 9),
            "proportional_term": round(proportional, 9),
            "integral_state": round(next_integral, 9),
            "integral_term": round(integral_term, 9),
            "derivative_error_c_per_s": round(derivative_error, 9),
            "derivative_term": round(derivative_term, 9),
            "raw_output_fraction": round(raw, 9),
            "output_fraction": round(output, 9),
            "reasons": reasons,
            "hardware_actuation": False,
            "runtime_pairing_with_alpha": False,
            "external_queries": 0,
            "external_actions": 0,
        }
        receipt["digest"] = _digest(receipt)
        return receipt


def feedforward_from_requirement(required_flow_lpm: float, design_flow_lpm: float) -> dict[str, Any]:
    required = _finite("required_flow_lpm", required_flow_lpm)
    design = _finite("design_flow_lpm", design_flow_lpm)
    if required < 0:
        raise ValueError("required_flow_lpm_must_be_non_negative")
    if design <= 0:
        raise ValueError("design_flow_lpm_must_be_positive")
    raw = required / design
    fraction = _clamp(raw, 0.0, 1.0)
    receipt = {
        "schema": "glaciereq.cooling-omega.feedforward.v1",
        "evidence_state": EVIDENCE_STATE,
        "required_flow_lpm": round(required, 9),
        "design_flow_lpm": round(design, 9),
        "raw_fraction": round(raw, 9),
        "feedforward_fraction": round(fraction, 9),
        "saturated": raw > 1.0,
        "runtime_pairing_with_alpha": False,
        "external_queries": 0,
        "external_actions": 0,
    }
    receipt["digest"] = _digest(receipt)
    return receipt


def simulate(
    temperatures_c: Iterable[float],
    *,
    config: PolicyConfig | None = None,
    dt: float = 1.0,
    feedforward_fraction: float = 0.0,
) -> dict[str, Any]:
    temperatures = list(temperatures_c)
    if not temperatures:
        raise ValueError("temperatures_required")
    policy = ResponsePolicy(config)
    steps = [policy.step(temp, dt=dt, feedforward_fraction=feedforward_fraction) for temp in temperatures]
    body: dict[str, Any] = {
        "schema": "glaciereq.cooling-omega.simulation.v1",
        "evidence_state": EVIDENCE_STATE,
        "target_c": policy.config.target_c,
        "feedforward_fraction": feedforward_fraction,
        "steps": steps,
        "outputs": [row["output_fraction"] for row in steps],
        "final_state": policy.state(),
        "hardware_actuation": False,
        "runtime_pairing_with_alpha": False,
        "external_queries": 0,
        "external_actions": 0,
    }
    body["digest"] = _digest(body)
    return body


class PID(ResponsePolicy):
    """Legacy facade preserving PID(...).step(temp, dt) -> float."""

    def __init__(self, kp: float = 0.08, ki: float = 0.02, kd: float = 0.01):
        super().__init__(PolicyConfig(kp=kp, ki=ki, kd=kd))

    def step(self, temp: float, dt: float = 1.0) -> float:  # type: ignore[override]
        return float(super().step(temp, dt=dt)["output_fraction"])


def control_loop(temps: Iterable[float]) -> dict[str, Any]:
    """Legacy facade with richer deterministic receipt fields added."""
    result = simulate(temps)
    return {
        "strand": "omega",
        "target_c": TARGET_C,
        "flows": result["outputs"],
        "evidence_state": EVIDENCE_STATE,
        "hardware_actuation": False,
        "runtime_pairing_with_alpha": False,
        "digest": result["digest"],
    }


if __name__ == "__main__":
    print(json.dumps(simulate([40.0, 43.0, 46.0, 44.0, 41.0], feedforward_fraction=0.5), indent=2, sort_keys=True))
