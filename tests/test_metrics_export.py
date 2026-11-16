import metrics_export


def test_export_rows_example():
    assert metrics_export.export_rows([("a", 1), ("b", 2)]) == "name,value\na,1\nb,2\n"


def test_export_rows_empty():
    assert metrics_export.export_rows([]) == "name,value\n"


def test_export_rows_negative_value():
    assert metrics_export.export_rows([("x", -3)]) == "name,value\nx,-3\n"
