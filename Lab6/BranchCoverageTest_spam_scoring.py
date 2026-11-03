import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ---------- score_message: word loop ----------
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0

def test_empty_text_scores_zero():
    assert score_message("", False, 0) == 0

def test_spam_word_case_insensitive():
    assert score_message("FREE", False, 0) == 2

def test_spam_word_with_punctuation_stripped():
    assert score_message("Winner! prize. cash,", False, 0) == 6

def test_uppercase_long_word_adds_one():
    assert score_message("HELLO", False, 0) == 1

def test_uppercase_length_boundary_four_adds_one():
    assert score_message("ABCD", False, 0) == 1

def test_uppercase_length_boundary_three_adds_nothing():
    assert score_message("ABC", False, 0) == 0

def test_short_uppercase_word_adds_nothing():
    assert score_message("HI", False, 0) == 0

def test_lowercase_non_spam_word_adds_nothing():
    assert score_message("hello", False, 0) == 0


# ---------- score_message: links ----------
def test_links_zero_adds_nothing():
    assert score_message("hello", False, 0) == 0

def test_links_one_adds_one():
    assert score_message("hello", False, 1) == 1

def test_links_boundary_three_adds_one():
    assert score_message("hello", False, 3) == 1

def test_links_boundary_four_adds_four():
    assert score_message("hello", False, 4) == 4


# ---------- score_message: known sender ----------
def test_unknown_sender_no_deduction():
    assert score_message("free free free", False, 0) == 6

def test_known_sender_deducts_three():
    assert score_message("free free free", True, 0) == 3

def test_known_sender_clamped_to_zero():
    assert score_message("hello", True, 0) == 0


# ---------- classify ----------
def test_classify_zero_is_clean():
    assert classify(0) == "clean"

def test_classify_three_is_clean():
    assert classify(3) == "clean"

def test_classify_four_is_suspicious():
    assert classify(4) == "suspicious"

def test_classify_seven_is_suspicious():
    assert classify(7) == "suspicious"

def test_classify_eight_is_spam():
    assert classify(8) == "spam"

def test_classify_high_is_spam():
    assert classify(20) == "spam"


# ---------- filter_inbox ----------
def test_filter_inbox_empty_list():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}

def test_filter_inbox_mixed():
    messages = [
        ("free prize winner cash", False, 5),  # 12 -> spam
        ("free free", False, 0),               # 4 -> suspicious
        ("hello", False, 0),                   # 0 -> clean
        ("free free free", True, 0),           # 3 -> clean
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 2}


# ---------- inbox_status ----------
def test_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"

def test_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"

def test_status_boundary_half_is_noisy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 1}) == "noisy"

def test_status_noisy():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 7}) == "noisy"

def test_status_boundary_fifth_is_healthy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 4}) == "healthy"

def test_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 4}) == "healthy"