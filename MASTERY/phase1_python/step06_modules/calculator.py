"""
calculator.py — ek simple MODULE

Module = ek .py file jisme reusable code ho.
"""

PI = 3.14159
MODULE_NAME = "Calculator"


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Zero se divide nahi kar sakte")
    return a / b


def percentage(value, percent):
    return (value * percent) / 100


class ScientificCalculator:
    """Module me class bhi ho sakti hai."""

    def power(self, base, exp):
        return base ** exp

    def square_root(self, n):
        if n < 0:
            raise ValueError("Negative number ka square root nahi")
        return n ** 0.5


# ==============================================================
# Ye block SIRF tab chalega jab file DIRECTLY run ho.
# Import karne pe NAHI chalega.
# ==============================================================
if __name__ == "__main__":
    print("calculator.py DIRECTLY chal rahi hai")
    print(f"__name__ = {__name__}")
    print(f"  add(2, 3)      = {add(2, 3)}")
    print(f"  divide(10, 4)  = {divide(10, 4)}")
    print(f"  percentage(50000, 10) = {percentage(50000, 10)}")
else:
    # Import hone pe ye chalega
    pass
