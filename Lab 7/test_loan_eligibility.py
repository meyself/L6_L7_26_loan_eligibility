from hypothesis import given, strategies as st
from loan_eligibility import parse_income, monthly_emi, pan_category, CATEGORIES

anything = st.one_of(st.none(), st.text(), st.integers(), st.floats(),
                     st.booleans(), st.lists(st.integers()))

# ---------- parse_income ----------
@given(anything)
def test_parse_income_no_crash(s):
    try:
        parse_income(s)
    except Exception as e:
        assert False, f"parse_income crashed with: {e!r}"

@given(st.text() | st.none())
def test_parse_income_returns_valid(s):
    result = parse_income(s)
    assert result is None or (isinstance(result, int) and result >= 0)

# ---------- monthly_emi ----------
@given(anything)
def test_monthly_emi_no_crash(s):
    try:
        monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed with: {e!r}"

@given(st.text(alphabet="0123456789,-. ", max_size=30))
def test_monthly_emi_digit_like_strings(s):
    try:
        result = monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed with: {e!r}"
    assert result is None or result >= 0

# ---------- pan_category ----------
@given(anything)
def test_pan_category_no_crash(s):
    try:
        pan_category(s)
    except Exception as e:
        assert False, f"pan_category crashed with: {e!r}"

@given(st.text() | st.none())
def test_pan_category_returns_valid(s):
    result = pan_category(s)
    assert result is None or result in CATEGORIES.values()

@given(st.from_regex(r"[A-Za-z]{5}[0-9]{4}[A-Za-z]", fullmatch=True))
def test_valid_pan_gets_category(pan):
    assert pan_category(pan) == CATEGORIES.get(pan[3].upper())