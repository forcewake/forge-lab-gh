import greeting


def test_module_exposes_functions():
    assert callable(greeting.greet)
    assert callable(greeting.farewell)
