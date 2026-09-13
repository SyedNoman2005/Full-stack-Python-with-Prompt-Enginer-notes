"""
================================================================
STEP 2 — FUNCTIONS
================================================================
Chalane ke liye:  python3 phase1_python/step02_functions.py

JOB LEVEL GOAL:
  "Function use karke code ko REUSABLE banana aana chahiye."

Ek hi code do jagah likh raha hai? -> Function bana de.
================================================================
"""


# ==============================================================
# 1. BASIC FUNCTION — tera wala example
# ==============================================================

def calculate_salary(basic, bonus):
    """Total salary = basic + bonus"""
    return basic + bonus


def basic_demo():
    print("\n--- 1. BASIC FUNCTION ---")

    salary = calculate_salary(30000, 5000)
    print(f"  calculate_salary(30000, 5000) = {salary}")

    # REUSABLE — yahi to poora point hai
    print("\n  Reusability (ek function, kayi baar use):")
    for basic, bonus in [(30000, 5000), (45000, 8000), (60000, 12000)]:
        print(f"    {basic} + {bonus} = {calculate_salary(basic, bonus)}")

    print("\n  return vs print:")
    print("    return -> value wapas deta hai, aage use kar sakte ho")
    print("    print  -> sirf screen pe dikhata hai, value kho jaati hai")
    print(f"    Proof: calculate_salary(1000,100) * 12 = {calculate_salary(1000, 100) * 12}")


# ==============================================================
# 2. PARAMETERS KE TYPES
# ==============================================================

def positional(a, b):
    """Order matter karta hai."""
    return a - b


def with_default(basic, bonus=0, tax=10):
    """Default value — na do to default use hoga."""
    total = basic + bonus
    return total - (total * tax / 100)


def with_args(*numbers):
    """*args -> kitne bhi arguments. Andar TUPLE ban jaata hai."""
    return sum(numbers)


def with_kwargs(**details):
    """**kwargs -> named arguments. Andar DICT ban jaata hai."""
    return ", ".join(f"{k}={v}" for k, v in details.items())


def everything(name, *skills, role="Developer", **extra):
    """Sahi order: normal -> *args -> default -> **kwargs"""
    return {
        "name": name,
        "skills": list(skills),
        "role": role,
        "extra": extra,
    }


def parameters_demo():
    print("\n--- 2. PARAMETER TYPES ---")

    print(f"  positional(10, 3)        = {positional(10, 3)}")
    print(f"  positional(3, 10)        = {positional(3, 10)}   <- order badla, answer badla")

    print(f"\n  keyword args (order matter nahi karta):")
    print(f"    positional(b=3, a=10)  = {positional(b=3, a=10)}")

    print(f"\n  default values:")
    print(f"    with_default(50000)                = {with_default(50000)}")
    print(f"    with_default(50000, 5000)          = {with_default(50000, 5000)}")
    print(f"    with_default(50000, 5000, tax=20)  = {with_default(50000, 5000, tax=20)}")

    print(f"\n  *args (variable number of arguments):")
    print(f"    with_args(1, 2, 3)          = {with_args(1, 2, 3)}")
    print(f"    with_args(10, 20, 30, 40)   = {with_args(10, 20, 30, 40)}")

    print(f"\n  **kwargs (named arguments):")
    print(f"    with_kwargs(name='Noman', city='Hyderabad')")
    print(f"    = {with_kwargs(name='Noman', city='Hyderabad')}")

    print(f"\n  Sab saath me:")
    result = everything("Noman", "Python", "SQL", "Django", role="Backend Dev", exp=0)
    for k, v in result.items():
        print(f"    {k:<7} : {v}")


# ==============================================================
# 3. MULTIPLE RETURN VALUES
# ==============================================================

def salary_stats(salaries):
    """Ek saath kai values return — andar TUPLE banta hai."""
    return min(salaries), max(salaries), sum(salaries) / len(salaries)


def multiple_return_demo():
    print("\n--- 3. MULTIPLE RETURN VALUES ---")

    salaries = [30000, 45000, 52000, 38000]
    lowest, highest, average = salary_stats(salaries)

    print(f"  salaries = {salaries}")
    print(f"  lowest   = {lowest}")
    print(f"  highest  = {highest}")
    print(f"  average  = {average:.2f}")
    print(f"\n  Actually ye tuple hai: {salary_stats(salaries)}")


# ==============================================================
# 4. SCOPE — Local vs Global (LEGB Rule)
# ==============================================================

company = "TechCorp"          # GLOBAL


def scope_demo():
    print("\n--- 4. SCOPE (LEGB) ---")

    def show_local():
        employee = "Noman"    # LOCAL — sirf is function ke andar
        print(f"    local  : {employee}")
        print(f"    global : {company}   <- global padh sakte hain")

    show_local()

    # Global ko BADALNE ke liye 'global' keyword chahiye
    counter = 0

    def increment_wrong():
        # counter += 1  -> ERROR! local variable referenced before assignment
        return counter + 1

    print(f"\n  LEGB = Local -> Enclosing -> Global -> Built-in")
    print(f"  Python isi order me variable dhoondhta hai.")
    print(f"  increment_wrong() = {increment_wrong()} (counter khud nahi badla: {counter})")

    # Sahi tareeka — return karo, global mat chhedo
    def increment_right(value):
        return value + 1

    counter = increment_right(counter)
    print(f"  Sahi tareeka: counter = increment_right(counter) -> {counter}")


# ==============================================================
# 5. LAMBDA + map / filter / sorted
# ==============================================================

def lambda_demo():
    print("\n--- 5. LAMBDA, MAP, FILTER ---")

    # Lambda = chhota, ek line ka, bina naam ka function
    square = lambda x: x ** 2
    add = lambda a, b: a + b

    print(f"  square(5)   = {square(5)}")
    print(f"  add(3, 7)   = {add(3, 7)}")

    nums = [1, 2, 3, 4, 5, 6]

    # MAP — har element pe function lagao
    doubled = list(map(lambda x: x * 2, nums))
    print(f"\n  map (double)  : {nums} -> {doubled}")

    # FILTER — condition pass karne wale hi rakho
    evens = list(filter(lambda x: x % 2 == 0, nums))
    print(f"  filter (even) : {nums} -> {evens}")

    # SORTED with key — ye real kaam me bahut aata hai
    employees = [
        {"name": "Noman", "salary": 30000},
        {"name": "Ali", "salary": 52000},
        {"name": "Sara", "salary": 45000},
    ]
    by_salary = sorted(employees, key=lambda e: e["salary"], reverse=True)
    print("\n  sorted by salary (high -> low):")
    for e in by_salary:
        print(f"    {e['name']:<6} {e['salary']}")

    print("\n  NOTE: List comprehension zyada Pythonic hai map/filter se:")
    print(f"    [x*2 for x in nums]           = {[x * 2 for x in nums]}")
    print(f"    [x for x in nums if x%2 == 0] = {[x for x in nums if x % 2 == 0]}")


# ==============================================================
# 6. RECURSION — function khud ko call kare
# ==============================================================

def factorial(n):
    """n! = n * (n-1)!"""
    if n <= 1:              # BASE CASE — ye na ho to infinite loop
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    """0, 1, 1, 2, 3, 5, 8, 13..."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def recursion_demo():
    print("\n--- 6. RECURSION ---")

    print(f"  factorial(5) = {factorial(5)}")
    print(f"  Fibonacci series: {[fibonacci(i) for i in range(10)]}")
    print("\n  YAAD RAKH: Base case bina recursion = infinite loop = crash")


# ==============================================================
# 7. DOCSTRING + TYPE HINTS (professional code)
# ==============================================================

def calculate_net_salary(basic: float, bonus: float = 0, tax_percent: float = 10) -> float:
    """
    Net salary nikalta hai tax kaatne ke baad.

    Args:
        basic:       Basic salary
        bonus:       Bonus amount (default 0)
        tax_percent: Tax percentage (default 10)

    Returns:
        Net salary tax kaatne ke baad

    Example:
        >>> calculate_net_salary(50000, 5000, 10)
        49500.0
    """
    gross = basic + bonus
    return gross - (gross * tax_percent / 100)


def professional_demo():
    print("\n--- 7. DOCSTRING + TYPE HINTS ---")
    print(f"  calculate_net_salary(50000, 5000) = {calculate_net_salary(50000, 5000)}")
    print("\n  Type hints code ko readable banate hain aur")
    print("  editor auto-complete + error catch karta hai.")
    print("  Har company ka codebase aise hi likha hota hai.")


# ==============================================================
# INTERVIEW QUESTIONS
# ==============================================================
INTERVIEW = """
Q1. Function kya hai aur kyun use karte hain?
    Reusable code block. DRY principle - Don't Repeat Yourself.
    Ek baar likho, baar baar use karo. Debug karna aasan.

Q2. *args vs **kwargs?
    *args    -> kitne bhi positional arguments  -> tuple banta hai
    **kwargs -> kitne bhi keyword arguments     -> dict banta hai

Q3. return vs print?
    return -> value wapas deta hai, aage use hoti hai
    print  -> sirf display, value kho jaati hai (None return hota hai)

Q4. Lambda kya hai? Kab use karein?
    Ek line ka anonymous function.
    sorted(), map(), filter() me chhota kaam karne ke liye.
    Bada logic ho to normal def use karo.

Q5. Local vs Global variable?
    Local  -> function ke andar, bahar accessible nahi
    Global -> poore file me accessible
    Global ko function ke andar badalne ke liye 'global' keyword chahiye

Q6. Default argument ka ek khatarnaak trap?
    def f(items=[]):  <- MUTABLE DEFAULT — sab calls me SAME list share hoti hai!
    Sahi: def f(items=None): if items is None: items = []

Q7. Recursion kya hai? Base case kyun zaroori hai?
    Function khud ko call kare. Base case na ho to
    infinite recursion -> RecursionError -> crash.

Q8. Python me function first-class object hai — matlab?
    Function ko variable me store kar sakte ho, argument me pass kar sakte ho,
    aur dusre function se return kar sakte ho.
"""


PRACTICE = """
1.  add(a, b) function banao jo do numbers ka sum de.
2.  is_even(n) banao jo True/False return kare.
3.  greet(name, greeting="Hello") — default argument use karo.
4.  total(*numbers) banao jo kitne bhi numbers ka sum de.
5.  Ek function jo list me se max aur min DONO return kare.
6.  calculate_tax(salary) — 30000 se kam pe 5%, upar 10%.
7.  Recursion se sum of first n numbers nikalo.
8.  Lambda + sorted se employees ko naam ke hisaab se sort karo.
9.  count_words(sentence) — har word kitni baar aaya, dict me do.
10. Ek function jo dusre function ko argument me le (higher-order function).
"""


if __name__ == "__main__":
    print("=" * 62)
    print("STEP 2 — FUNCTIONS")
    print("=" * 62)

    basic_demo()
    parameters_demo()
    multiple_return_demo()
    scope_demo()
    lambda_demo()
    recursion_demo()
    professional_demo()

    print("\n" + "=" * 62)
    print("INTERVIEW QUESTIONS")
    print("=" * 62)
    print(INTERVIEW)

    print("=" * 62)
    print("PRACTICE")
    print("=" * 62)
    print(PRACTICE)
