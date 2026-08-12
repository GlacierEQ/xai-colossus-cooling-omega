from __future__ import annotations

import pytest

from flow_controller import PID, PolicyConfig, ResponsePolicy, control_loop, feedforward_from_requirement, simulate


def test_first_sample_has_no_derivative_kick() -> None:
    policy = ResponsePolicy(PolicyConfig(target_c=42.0, kp=0.08, ki=0.02, kd=0.5))
    receipt = policy.step(46.0, dt=1.0, feedforward_fraction=0.2)
    assert receipt["derivative_error_c_per_s"] == 0.0
    assert receipt["derivative_term"] == 0.0


def test_hotter_sequence_increases_modeled_demand() -> None:
    result = simulate([40.0, 43.0, 46.0], feedforward_fraction=0.4)
    assert result["outputs"][2] > result["outputs"][0]
    assert all(0.0 <= value <= 1.0 for value in result["outputs"])


def test_integral_is_bounded() -> None:
    policy = ResponsePolicy(PolicyConfig(integral_limit=2.0))
    for _ in range(20):
        receipt = policy.step(60.0)
    assert receipt["integral_state"] == 2.0
    assert "INTEGRAL_CLAMPED" in receipt["reasons"]


def test_reset_clears_state() -> None:
    policy = ResponsePolicy()
    policy.step(50.0)
    policy.reset()
    assert policy.state() == {"integral": 0.0, "previous_error_c": None, "step_index": 0}


def test_feedforward_bridge_is_data_only_and_bounded() -> None:
    receipt = feedforward_from_requirement(48_000.0, 60_000.0)
    assert receipt["feedforward_fraction"] == 0.8
    assert receipt["runtime_pairing_with_alpha"] is False
    saturated = feedforward_from_requirement(72_000.0, 60_000.0)
    assert saturated["feedforward_fraction"] == 1.0
    assert saturated["saturated"] is True


def test_legacy_pid_and_control_loop_remain_usable() -> None:
    pid = PID()
    assert 0.0 <= pid.step(45.0) <= 1.0
    result = control_loop([40.0, 45.0])
    assert result["strand"] == "omega"
    assert len(result["flows"]) == 2
    assert result["hardware_actuation"] is False
