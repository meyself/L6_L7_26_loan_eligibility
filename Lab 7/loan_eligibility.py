import re

CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}
PAN_PATTERN = re.compile(r"[A-Za-z]{5}[0-9]{4}[A-Za-z]")


def _to_int(text):
    """Strict non-negative integer parser. Returns None if invalid."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not text or not text.isascii() or not text.isdigit() or len(text) > 18:
        return None
    return int(text)


def parse_income(income):
    if not isinstance(income, str):
        return None
    return _to_int(income.replace(',', ''))


def monthly_emi(details):
    if not isinstance(details, str):
        return None
    parts = details.split(',')
    if len(parts) != 3:
        return None
    principal, rate, years = (_to_int(p) for p in parts)
    if principal is None or rate is None or years is None:
        return None
    if principal <= 0 or principal > 10**12 or years <= 0 or years > 100 or rate > 100:
        return None
    n = years * 12
    if rate == 0:
        return round(principal / n, 2)
    r = rate / 1200
    try:
        factor = (1 + r) ** n
        return round(principal * r * factor / (factor - 1), 2)
    except (OverflowError, ZeroDivisionError):
        return None


def pan_category(pan):
    if not isinstance(pan, str):
        return None
    pan = pan.strip()
    if not PAN_PATTERN.fullmatch(pan):
        return None
    return CATEGORIES.get(pan[3].upper())


def main():
    print("==== Running parse_income ====")
    result = parse_income(input("Enter monthly income (e.g. 50,000): "))
    print("Income:", result if result is not None else "Invalid income")

    print("\n==== Running monthly_emi ====")
    result = monthly_emi(input("Enter principal,rate,years (e.g. 500000,10,5): "))
    print("Monthly EMI:", result if result is not None else "Invalid input")

    print("\n==== Running pan_category ====")
    result = pan_category(input("Enter a PAN number (e.g. ABCPE1234F): "))
    print("PAN Category:", result if result is not None else "Invalid PAN")


if __name__ == "__main__":
    main()