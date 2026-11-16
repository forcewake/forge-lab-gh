import textstats


def test_word_count_normal_sentence():
    assert textstats.word_count("hello big world") == 3


def test_word_count_extra_whitespace():
    assert textstats.word_count("  spaced   out  ") == 2


def test_word_count_empty_string():
    assert textstats.word_count("") == 0
