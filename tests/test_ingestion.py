from app.simulator import simulate_rounds


def test_simulation_reproducible():
    first = simulate_rounds(3, 2, 100.0, 1.0, 200, seed=42, strategy="flat")
    second = simulate_rounds(3, 2, 100.0, 1.0, 200, seed=42, strategy="flat")
    assert first == second
