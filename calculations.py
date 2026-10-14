"""Simple, transparent deposit arithmetic in rupees; illustrations, not financial advice."""


def inr(amount):
    """Format rupees with Indian grouping, e.g. 1234567 -> '₹12,34,567'."""
    sign = "-" if amount < 0 else ""
    digits = str(round(abs(amount)))
    if len(digits) > 3:
        head, tail = digits[:-3], digits[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        digits = ",".join([head] + groups + [tail])
    return f"{sign}₹{digits}"


def fd_maturity(principal, rate_percent, years, times_per_year=4):
    """Fixed deposit value at maturity; Indian banks usually compound quarterly."""
    return principal * (1 + rate_percent / (100 * times_per_year)) ** (times_per_year * years)


def interest_payout(principal, rate_percent, payouts_per_year=12):
    """Interest paid out each period when interest is not reinvested (e.g. monthly FD, quarterly SCSS)."""
    return principal * rate_percent / (100 * payouts_per_year)


def life_certificate_window(age):
    """When a central government pensioner submits the yearly life certificate."""
    if age >= 80:
        return "1 October to 30 November"
    return "1 November to 30 November"
