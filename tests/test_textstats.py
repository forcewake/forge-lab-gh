import textstats


def test_word_count_simple():
    assert textstats.word_count("hello big world") == 3


def test_word_count_irregular_whitespace():
    assert textstats.word_count("  spaced   out  ") == 2


def test_word_count_empty():
    assert textstats.word_count("") == 0
