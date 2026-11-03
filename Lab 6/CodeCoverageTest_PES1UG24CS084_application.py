import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate

#Example test cases:
def test_excellent_band():
    assert credit_band(800) == "excellent"

def test_eligible():
    assert is_eligible(30, 50000, "salaried", 800) is True

#Write the rest of the test cases so that the code is 90- 100% covered.

# 1. credit_band: invalid scores (both ends) + good / fair / poor branches
def test_credit_band_other_bands_and_invalid():
    assert credit_band(700) == "good"
    assert credit_band(600) == "fair"
    assert credit_band(400) == "poor"
    with pytest.raises(ValueError):
        credit_band(299)
    with pytest.raises(ValueError):
        credit_band(901)

# 2. is_eligible: every rejection path
def test_is_eligible_rejections():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "student", 800)           # unknown employment
    assert is_eligible(20, 50000, "salaried", 800) is False        # too young
    assert is_eligible(61, 50000, "salaried", 800) is False        # too old
    assert is_eligible(30, 20000, "salaried", 800) is False        # low income
    assert is_eligible(30, 50000, "salaried", 400) is False        # poor credit band

# 3. interest_rate: all bands, self-employed surcharge, collateral discount
def test_interest_rate_combinations():
    assert interest_rate(800, "salaried", False) == 8          # excellent
    assert interest_rate(700, "self_employed", False) == 11    # good + 1
    assert interest_rate(600, "salaried", True) == 11          # fair 13 - 2
