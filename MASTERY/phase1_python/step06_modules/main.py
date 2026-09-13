"""
================================================================
STEP 6 — MODULES + PACKAGES  🟡
================================================================
Chalane ke liye:  python3 phase1_python/step06_modules/main.py

Practical level bas — deep theory ki zarurat nahi.
================================================================
"""

import sys
from pathlib import Path

# Is folder ko import path me daalo taaki kahin se bhi chal sake
sys.path.insert(0, str(Path(__file__).parent))

# ---- IMPORT KE ALAG ALAG TAREEKE ----

# 1. Poora module
import calculator

# 2. Module with ALIAS
import calculator as calc

# 3. Specific cheezein
from calculator import add, divide, PI

# 4. Function with alias
from calculator import multiply as times

# 5. Class import
from calculator import ScientificCalculator

# 6. PACKAGE se import (__init__.py ki wajah se ye seedha milta hai)
from employee_package import Employee, Manager, format_salary, calculate_tax

# 7. Package ke andar ke module se seedha
from employee_package.utils import net_salary

# 8. Built-in modules
import math
import random
from datetime import datetime


def import_styles_demo():
    print("\n--- 1. IMPORT KE TAREEKE ---")

    print(f"  import calculator           -> calculator.add(2,3)  = {calculator.add(2, 3)}")
    print(f"  import calculator as calc   -> calc.subtract(10,4)  = {calc.subtract(10, 4)}")
    print(f"  from calculator import add  -> add(5,5)             = {add(5, 5)}")
    print(f"  from ... import multiply as times -> times(3,4)     = {times(3, 4)}")
    print(f"  from calculator import PI   -> PI                   = {PI}")

    sci = ScientificCalculator()
    print(f"  Class import                -> sci.power(2, 10)     = {sci.power(2, 10)}")
    print(f"                              -> sci.square_root(144) = {sci.square_root(144)}")

    print("\n  ⚠️  from calculator import *   <- ye MAT karo")
    print("     Naam clash hote hain, pata nahi chalta kya import hua.")


def package_demo():
    print("\n--- 2. PACKAGE ---")

    print("  Package = folder with __init__.py")
    print("  employee_package/")
    print("    ├── __init__.py    <- isse package banta hai")
    print("    ├── models.py      <- classes")
    print("    └── utils.py       <- helper functions")

    emp = Employee("Noman", 30000, "IT")
    mgr = Manager("Sara", 80000, "IT", 5)

    print(f"\n  {emp}")
    print(f"  {mgr}")

    print(f"\n  format_salary(30000)       = {format_salary(30000)}")
    print(f"  calculate_tax(30000, 10)   = {calculate_tax(30000, 10)}")
    print(f"  net_salary(30000)          = {net_salary(30000)}")

    import employee_package
    print(f"\n  Package version: {employee_package.PACKAGE_VERSION}")

    print("\n  __init__.py ka faida:")
    print("    from employee_package import Employee     <- saaf")
    print("    (bina __init__.py ke: from employee_package.models import Employee)")


def dunder_name_demo():
    print("\n--- 3. __name__ == '__main__'  (ZAROOR SAMAJH) ---")

    print(f"\n  Is file ka __name__     = '{__name__}'")
    print(f"  calculator ka __name__  = '{calculator.__name__}'")

    print("""
  RULE:
    File DIRECTLY chalao   ->  __name__ = "__main__"
    File IMPORT karo       ->  __name__ = "module_ka_naam"

  Isiliye har file me ye likhte hain:

    if __name__ == "__main__":
        # test/demo code
        # ye SIRF direct run pe chalega, import pe nahi

  PROOF: calculator.py me bhi ye block hai. Par upar humne
  use IMPORT kiya, isliye uska test code NAHI chala.
  Agar chalana ho: python3 calculator.py
    """)


def builtin_modules_demo():
    print("\n--- 4. BUILT-IN MODULES (batteries included) ---")

    print(f"  math.sqrt(144)   = {math.sqrt(144)}")
    print(f"  math.ceil(4.1)   = {math.ceil(4.1)}")
    print(f"  math.floor(4.9)  = {math.floor(4.9)}")
    print(f"  math.pi          = {math.pi:.5f}")

    random.seed(42)     # seed = har baar same result (testing ke liye)
    print(f"\n  random.randint(1,100) = {random.randint(1, 100)}")
    print(f"  random.choice([...])  = {random.choice(['Python', 'SQL', 'Django'])}")

    print(f"\n  datetime.now().year   = {datetime.now().year}")

    print("\n  Python me 200+ built-in modules hain.")
    print("  Isiliye kehte hain: 'Python comes with batteries included'")


def module_search_demo():
    print("\n--- 5. PYTHON MODULE KAHAN DHOONDHTA HAI? ---")

    print("  sys.path me — is order me:")
    print("    1. Current directory (jahan se script chali)")
    print("    2. PYTHONPATH environment variable")
    print("    3. Standard library")
    print("    4. site-packages (pip se install kiye hue)")

    print(f"\n  Pehle 3 paths abhi:")
    for p in sys.path[:3]:
        print(f"    {p or '(current directory)'}")


INTERVIEW = """
Q1. Module kya hai?
    Ek .py file jisme functions, classes, variables hote hain.
    Code ko organize aur reuse karne ke liye.

Q2. Package kya hai?
    Modules ka folder. __init__.py hoti hai usme.

Q3. __init__.py ka kaam?
    Folder ko package banati hai. Package-level imports define karti hai.
    Python 3.3+ me technically optional, par likhna best practice.

Q4. import * kyun bura hai?
    Naam clash, unclear code, editor auto-complete toot jaata hai.

Q5. __name__ == "__main__" kyun?
    Taaki import karne pe test code na chale.

Q6. Absolute vs Relative import?
    Absolute: from employee_package.models import Employee
    Relative: from .models import Employee      (package ke andar)
    Absolute prefer karo — saaf aur clear hota hai.

Q7. Python module kahan se load karta hai?
    sys.path se — current dir, PYTHONPATH, stdlib, site-packages.

Q8. Circular import kya hai?
    A, B ko import kare aur B, A ko. Error aata hai.
    Solution: code restructure karo ya function ke andar import karo.
"""


if __name__ == "__main__":
    print("=" * 62)
    print("STEP 6 — MODULES + PACKAGES")
    print("=" * 62)

    import_styles_demo()
    package_demo()
    dunder_name_demo()
    builtin_modules_demo()
    module_search_demo()

    print("\n" + "=" * 62)
    print("INTERVIEW QUESTIONS")
    print("=" * 62)
    print(INTERVIEW)
