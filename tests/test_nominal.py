from flow_controller import simulate


def test_nominal_simulation_is_local_and_deterministic_shape() -> None:
    result = simulate([40.0, 43.0, 46.0], feedforward_fraction=0.5)
    assert len(result["steps"]) == 3
    assert result["hardware_actuation"] is False
    assert result["runtime_pairing_with_alpha"] is False
    assert result["external_queries"] == 0
    assert result["external_actions"] == 0
    assert len(result["digest"]) == 64
