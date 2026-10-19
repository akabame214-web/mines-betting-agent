from app.probability import survival_probability


def test_three_mines_two_clicks():
    result = survival_probability(3, 2)
    assert abs(result - 0.77) < 1e-9


def test_five_mines_two_clicks():
    result = survival_probability(5, 2)
    assert abs(result - 0.6333333333333333) < 1e-9


def test_ten_mines_two_clicks():
    result = survival_probability(10, 2)
    assert abs(result - 0.35) < 1e-9


def test_invalid_inputs():
    try:
        survival_probability(25, 1)
        raise AssertionError("Expected ValueError for invalid mine count")
    except ValueError:
        pass

    try:
        survival_probability(3, 24)
        raise AssertionError("Expected ValueError for impossible safe click target")
    except ValueError:
        pass
