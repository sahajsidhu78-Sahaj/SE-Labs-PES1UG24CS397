from hypothesis import given, strategies as st
from spam_scoring import sender_domain, first_link, shout_ratio


@given(st.text() | st.none())
def test_sender_domain_no_crash(s):
    try:
        sender_domain(s)
    except Exception as e:
        assert False, f"sender_domain crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_first_link_no_crash(s):
    try:
        first_link(s)
    except Exception as e:
        assert False, f"first_link crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_shout_ratio_no_crash(s):
    try:
        shout_ratio(s)
    except Exception as e:
        assert False, f"shout_ratio crashed with: {e!r} for input {s!r}"


# ---------- extra property checks (return values stay sensible) ----------
@given(st.text() | st.none())
def test_sender_domain_returns_lowercase_string_without_at(s):
    result = sender_domain(s)
    assert isinstance(result, str)
    assert result == result.lower()
    assert "@" not in result


@given(st.text() | st.none())
def test_first_link_returns_empty_or_http_link(s):
    result = first_link(s)
    assert isinstance(result, str)
    assert result == "" or result.startswith(("http://", "https://"))


@given(st.text() | st.none())
def test_shout_ratio_is_between_zero_and_one(s):
    result = shout_ratio(s)
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0