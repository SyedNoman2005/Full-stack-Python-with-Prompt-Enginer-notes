"""
================================================================
STEP 4 — EXCEPTION HANDLING  🔴🔴
================================================================
Chalane ke liye:  python3 phase1_python/step04_exceptions.py

Bina exception handling ke app ek galat input pe CRASH ho jaata hai.
Production code me har risky line try/except me hoti hai.
================================================================
"""


# ==============================================================
# 1. BASIC try / except — tera wala example
# ==============================================================

def safe_divide(user_input):
    """
    Tera diya hua example — input() ki jagah parameter,
    taaki file automatically chal sake.
    """
    try:
        number = int(user_input)
        result = 100 / number
        return f"100 / {number} = {result}"

    except ValueError:
        return "Enter a valid number"

    except ZeroDivisionError:
        return "Cannot divide by zero"


def basic_demo():
    print("\n--- 1. BASIC try / except ---")

    for value in ["5", "abc", "0", "25"]:
        print(f'  input "{value:<4}" -> {safe_divide(value)}')

    print("\n  Bina try/except ke ye program CRASH ho jaata.")
    print("  Try/except ke saath -> user ko friendly message milta hai.")


# ==============================================================
# 2. POORA STRUCTURE — try / except / else / finally
# ==============================================================

def full_structure(value):
    """
    try     -> risky code
    except  -> error aaye to kya karein
    else    -> KOI error NA aaye to chalega
    finally -> HAMESHA chalega (error ho ya na ho)
    """
    log = []
    try:
        log.append("try: conversion shuru")
        number = int(value)
        result = 100 / number

    except ValueError:
        log.append("except: ValueError pakda")
        result = None

    except ZeroDivisionError:
        log.append("except: ZeroDivisionError pakda")
        result = None

    else:
        log.append(f"else: koi error nahi, result = {result}")

    finally:
        log.append("finally: cleanup (ye HAMESHA chalta hai)")

    return log


def structure_demo():
    print("\n--- 2. try / except / else / finally ---")

    for value in ["4", "xyz", "0"]:
        print(f'\n  Input: "{value}"')
        for line in full_structure(value):
            print(f"    {line}")

    print("\n  FINALLY ka asli use:")
    print("    - File band karna")
    print("    - Database connection close karna")
    print("    - Lock release karna")
    print("    Ye cheezein error aane pe BHI honi chahiye.")


# ==============================================================
# 3. COMMON EXCEPTIONS — ye sab yaad rakhne hain
# ==============================================================

def common_exceptions_demo():
    print("\n--- 3. COMMON EXCEPTIONS ---")

    tests = [
        ("ValueError",        lambda: int("abc")),
        ("ZeroDivisionError", lambda: 10 / 0),
        ("TypeError",         lambda: "5" + 5),
        ("IndexError",        lambda: [1, 2, 3][10]),
        ("KeyError",          lambda: {"a": 1}["b"]),
        ("AttributeError",    lambda: "text".push()),
        ("FileNotFoundError", lambda: open("nahi_hai.txt")),
        ("NameError",         lambda: undefined_variable),  # noqa: F821
    ]

    for name, fn in tests:
        try:
            fn()
        except Exception as e:
            print(f"  {name:<20} -> {type(e).__name__}: {e}")


# ==============================================================
# 4. MULTIPLE EXCEPTIONS + generic except
# ==============================================================

def multiple_exceptions_demo():
    print("\n--- 4. MULTIPLE EXCEPTIONS ---")

    def process(data, key, divisor):
        try:
            value = data[key]
            return value / divisor

        # Ek saath kai exceptions — tuple me
        except (KeyError, IndexError) as e:
            return f"Data problem: {type(e).__name__}"

        except ZeroDivisionError:
            return "Zero se divide nahi kar sakte"

        # GENERIC — sabse LAST me, warna baaki kabhi nahi chalenge
        except Exception as e:
            return f"Unexpected: {type(e).__name__}: {e}"

    data = {"salary": 30000}
    print(f"  process(data, 'salary', 12)  -> {process(data, 'salary', 12)}")
    print(f"  process(data, 'bonus', 12)   -> {process(data, 'bonus', 12)}")
    print(f"  process(data, 'salary', 0)   -> {process(data, 'salary', 0)}")
    print(f"  process(data, 'salary', 'a') -> {process(data, 'salary', 'a')}")

    print("\n  ORDER MATTERS: specific pehle, generic baad me.")
    print("  Galat: except Exception upar rakh do -> baaki kabhi nahi chalenge.")

    print("\n  KABHI MAT KARO:")
    print("    except:           <- bare except, Ctrl+C bhi pakad leta hai")
    print("    except: pass      <- error chhupa diya, debugging namumkin")


# ==============================================================
# 5. raise — khud error phenko
# ==============================================================

def validate_salary(salary):
    """Validation me raise use karte hain."""
    if not isinstance(salary, (int, float)):
        raise TypeError("Salary number honi chahiye")
    if salary < 0:
        raise ValueError("Salary negative nahi ho sakti")
    if salary > 10_000_000:
        raise ValueError("Salary bahut zyada hai, dobara check karo")
    return f"Valid salary: {salary}"


def validate_age(age):
    if age < 18:
        raise ValueError(f"Age {age} — minimum 18 chahiye")
    return f"Age {age} OK"


def raise_demo():
    print("\n--- 5. raise (khud error phenko) ---")

    for salary in [30000, -500, "abc", 99_999_999]:
        try:
            print(f"  {validate_salary(salary)}")
        except (TypeError, ValueError) as e:
            print(f"  {type(e).__name__}: {e}")

    print("\n  RE-RAISE (log karo, phir upar bhejo):")
    def process():
        try:
            validate_age(15)
        except ValueError as e:
            print(f"    [LOG] Error hua: {e}")
            raise           # dobara phenk do, caller handle kare

    try:
        process()
    except ValueError:
        print("    [CALLER] Error yahan pakda gaya")

    print("\n  raise ... from ... (exception chaining):")
    try:
        try:
            int("abc")
        except ValueError as e:
            raise RuntimeError("Employee data process nahi hua") from e
    except RuntimeError as e:
        print(f"    {e}")
        print(f"    Original cause: {type(e.__cause__).__name__}")


# ==============================================================
# 6. CUSTOM EXCEPTIONS — professional code
# ==============================================================

class EmployeeError(Exception):
    """Base exception — saare employee errors ka parent"""
    pass


class InvalidSalaryError(EmployeeError):
    def __init__(self, salary, message="Salary invalid hai"):
        self.salary = salary
        self.message = f"{message}: {salary}"
        super().__init__(self.message)


class EmployeeNotFoundError(EmployeeError):
    def __init__(self, emp_id):
        self.emp_id = emp_id
        super().__init__(f"Employee ID {emp_id} nahi mila")


class InsufficientBalanceError(Exception):
    def __init__(self, balance, requested):
        self.shortfall = requested - balance
        super().__init__(
            f"Balance {balance}, maanga {requested}, kam pad raha {self.shortfall}"
        )


def custom_exception_demo():
    print("\n--- 6. CUSTOM EXCEPTIONS ---")

    db = {1: "Noman", 2: "Ali"}

    def get_employee(emp_id):
        if emp_id not in db:
            raise EmployeeNotFoundError(emp_id)
        return db[emp_id]

    def set_salary(salary):
        if salary < 0:
            raise InvalidSalaryError(salary, "Negative salary allowed nahi")
        return salary

    for emp_id in [1, 99]:
        try:
            print(f"  get_employee({emp_id}) -> {get_employee(emp_id)}")
        except EmployeeNotFoundError as e:
            print(f"  EmployeeNotFoundError: {e}")

    try:
        set_salary(-1000)
    except InvalidSalaryError as e:
        print(f"  InvalidSalaryError: {e}  (salary attribute: {e.salary})")

    try:
        raise InsufficientBalanceError(5000, 8000)
    except InsufficientBalanceError as e:
        print(f"  InsufficientBalanceError: {e}")
        print(f"    e.shortfall = {e.shortfall}")

    print("\n  Base class se sab pakad sakte ho:")
    for err in [EmployeeNotFoundError(5), InvalidSalaryError(-1)]:
        try:
            raise err
        except EmployeeError as e:
            print(f"    EmployeeError pakda -> {type(e).__name__}")


# ==============================================================
# 7. REAL WORLD PATTERNS
# ==============================================================

def real_world_demo():
    print("\n--- 7. REAL WORLD PATTERNS ---")

    # Pattern 1: with statement — auto cleanup
    print("\n  Pattern 1: 'with' (file khud band hoti hai)")
    print("    with open('file.txt') as f:")
    print("        data = f.read()")
    print("    # error aaye ya na aaye, file band ho jaati hai")

    # Pattern 2: Retry logic
    print("\n  Pattern 2: Retry logic (API call ke liye)")
    attempts = 0

    def flaky_operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Network down")
        return "Success!"

    for attempt in range(1, 5):
        try:
            result = flaky_operation()
            print(f"    Attempt {attempt}: {result}")
            break
        except ConnectionError as e:
            print(f"    Attempt {attempt}: {e} — retry...")

    # Pattern 3: Default value on failure
    print("\n  Pattern 3: Fail hone pe default value")

    def safe_int(value, default=0):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    for v in ["42", "abc", None, "7"]:
        print(f"    safe_int({str(v):<6}) = {safe_int(v)}")

    # Pattern 4: Input validation loop (real app me aise hota hai)
    print("\n  Pattern 4: Input loop (real app)")
    print("    while True:")
    print("        try:")
    print("            age = int(input('Age: '))")
    print("            if age < 0: raise ValueError('Negative')")
    print("            break")
    print("        except ValueError as e:")
    print("            print('Galat input, dobara try karo')")


# ==============================================================
# INTERVIEW
# ==============================================================
INTERVIEW = """
Q1. Exception handling kyun zaroori hai?
    Program crash na ho. User ko friendly message mile.
    Resources (file, DB connection) properly close hon.

Q2. Error vs Exception?
    Error     -> serious, handle nahi kar sakte (MemoryError, SyntaxError)
    Exception -> runtime me aati hai, handle kar sakte hain

Q3. else block kab chalta hai?
    Jab try block me KOI exception NA aaye.
    Use: risky code try me rakho, success wala code else me.

Q4. finally kab chalta hai?
    HAMESHA. Error aaye, na aaye, ya return bhi ho jaye — finally chalta hai.
    Cleanup ke liye (file close, DB disconnect).

Q5. raise kya karta hai?
    Manually exception phenkta hai. Validation me use hota hai.

Q6. Custom exception kaise banate hain?
    class MyError(Exception): pass
    Phir raise MyError("message")

Q7. except: aur except Exception: me kya fark?
    except:           -> SAB kuch pakadta hai, KeyboardInterrupt/SystemExit bhi. BURA.
    except Exception: -> sirf normal exceptions. Behtar.

Q8. Multiple exceptions ek saath kaise?
    except (ValueError, TypeError) as e:

Q9. Exception order kaise likhein?
    Specific pehle, generic baad me.
    Warna generic sab pakad lega aur specific kabhi nahi chalega.

Q10. try/except performance pe asar?
    Exception NA aaye to almost zero cost.
    Exception aaye to thoda slow. Isliye normal flow me exception mat use karo.

Q11. Common exceptions ke naam batao?
    ValueError, TypeError, KeyError, IndexError, AttributeError,
    ZeroDivisionError, FileNotFoundError, NameError, ImportError
"""


PRACTICE = """
1.  User input ko int me convert karo, galat ho to message do. (tera wala)
2.  Do numbers divide karo, zero division handle karo.
3.  File open karo jo exist nahi karti — FileNotFoundError handle karo.
4.  Dict me missing key access karo — KeyError handle karo.
5.  Custom exception NegativeSalaryError banao aur use karo.
6.  Ek function jo age validate kare (18+), warna ValueError raise kare.
7.  finally use karke "Program end" print karo har case me.
8.  Calculator banao jo har galat input handle kare aur crash na ho.
9.  Retry logic likho — 3 baar try kare phir haar maane.
10. Nested try/except likho aur dekho kaunsa pehle chalta hai.
"""


if __name__ == "__main__":
    print("=" * 62)
    print("STEP 4 — EXCEPTION HANDLING")
    print("=" * 62)

    basic_demo()
    structure_demo()
    common_exceptions_demo()
    multiple_exceptions_demo()
    raise_demo()
    custom_exception_demo()
    real_world_demo()

    print("\n" + "=" * 62)
    print("INTERVIEW QUESTIONS")
    print("=" * 62)
    print(INTERVIEW)

    print("=" * 62)
    print("PRACTICE")
    print("=" * 62)
    print(PRACTICE)
