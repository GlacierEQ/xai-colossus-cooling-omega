from flow_controller import ResponsePolicy


def test_extreme_heat_saturates_modeled_output_without_emergency_action() -> None:
    result = ResponsePolicy().step(100.0)
    assert result["output_fraction"] == 1.0
    assert "SATURATED_HIGH" in result["reasons"]
    assert result["hardware_actuation"] is False
    assert result["external_actions"] == 0
