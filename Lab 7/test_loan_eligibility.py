from hypothesis import given, strategies as st
from loan_eligibility import parse_income, monthly_emi, pan_category

@given(st.text() | st.none())
def test_parse_income_no_crash(s):

@given(st.text() | st.none())
def test_monthly_emi_no_crash(s):

@given(st.text() | st.none())
def test_pan_category_no_crash(s):
