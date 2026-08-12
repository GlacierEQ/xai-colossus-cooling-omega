from flow_controller import simulate


def test_simulation_receipt_is_deterministic() -> None:
    first = simulate([40.0, 43.0, 46.0], feedforward_fraction=0.5)
    second = simulate([40.0, 43.0, 46.0], feedforward_fraction=0.5)
    assert first == second
    assert first["digest"] == second["digest"]
