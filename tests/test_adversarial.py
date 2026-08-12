from __future__ import annotations

import pytest

from flow_controller import PolicyConfig, ResponsePolicy, feedforward_from_requirement, simulate


def test_non_finite_temperature_refuses() -> None:
    with pytest.raises(ValueError, match="temperature_c_must_be_finite"):
        ResponsePolicy().step(float("nan"))


def test_non_positive_dt_refuses_instead_of_dividing_by_epsilon() -> None:
    with pytest.raises(ValueError, match="dt_must_be_positive"):
        ResponsePolicy().step(45.0, dt=0.0)
    with pytest.raises(ValueError, match="dt_must_be_positive"):
        ResponsePolicy().step(45.0, dt=-1.0)


def test_bad_feedforward_refuses() -> None:
    with pytest.raises(ValueError, match="feedforward_fraction_must_be_between_zero_and_one"):
        ResponsePolicy().step(45.0, feedforward_fraction=1.1)


def test_bad_config_refuses() -> None:
    with pytest.raises(ValueError, match="gains_must_be_non_negative"):
        ResponsePolicy(PolicyConfig(kp=-0.1))


def test_bad_flow_bridge_refuses() -> None:
    with pytest.raises(ValueError, match="required_flow_lpm_must_be_non_negative"):
        feedforward_from_requirement(-1.0, 10.0)
    with pytest.raises(ValueError, match="design_flow_lpm_must_be_positive"):
        feedforward_from_requirement(1.0, 0.0)


def test_empty_simulation_refuses() -> None:
    with pytest.raises(ValueError, match="temperatures_required"):
        simulate([])
