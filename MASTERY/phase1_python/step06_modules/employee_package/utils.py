"""
employee_package/utils.py — helper functions yahan

Django projects me bhi utils.py bahut common hai.
"""


def format_salary(amount, currency="INR"):
    """30000 -> 'INR 30,000'"""
    return f"{currency} {amount:,}"


def calculate_tax(salary, percent=10):
    """Tax nikalo"""
    return round(salary * percent / 100, 2)


def net_salary(salary, tax_percent=10):
    """Tax ke baad ki salary"""
    return salary - calculate_tax(salary, tax_percent)
