"""
================================================================
STEP 1 — PYTHON BASICS
================================================================
Chalane ke liye:  python3 phase1_python/step01_basics.py

Ye sabse neeche wali foundation hai. Isko kaccha chhoda to
OOP aur Django me har jagah dikkat aayegi.
================================================================
"""


# ==============================================================
# 1. VARIABLES aur DATA TYPES
# ==============================================================
# Python me type declare nahi karte. Value se type khud bante hai.

def variables_demo():
    print("\n--- 1. VARIABLES & DATA TYPES ---")

    name = "Noman"          # str
    age = 21                # int
    salary = 30000.50       # float
    is_employed = True      # bool
    nothing = None          # NoneType

    print(f"name    = {name}    -> {type(name).__name__}")
    print(f"age     = {age}       -> {type(age).__name__}")
    print(f"salary  = {salary}  -> {type(salary).__name__}")
    print(f"working = {is_employed}     -> {type(is_employed).__name__}")
    print(f"nothing = {nothing}     -> {type(nothing).__name__}")

    # TYPE CASTING — ek type ko dusre me badalna
    print("\nType Casting:")
    print(f'  int("100")   = {int("100")}')
    print(f'  float("3.5") = {float("3.5")}')
    print(f'  str(500)     = "{str(500)}"')
    print(f'  bool(0)      = {bool(0)}      <- 0, "", [], None sab False hain')
    print(f'  bool("hi")   = {bool("hi")}')

    # INTERVIEW: input() hamesha STRING deta hai
    # age = input("Age: ")      -> ye string hai
    # age = int(input("Age: ")) -> ye number hai. Ye galti sab karte hain.


# ==============================================================
# 2. OPERATORS
# ==============================================================

def operators_demo():
    print("\n--- 2. OPERATORS ---")

    a, b = 17, 5

    print("Arithmetic:")
    print(f"  {a} + {b}  = {a + b}")
    print(f"  {a} - {b}  = {a - b}")
    print(f"  {a} * {b}  = {a * b}")
    print(f"  {a} / {b}  = {a / b}     <- / hamesha float deta hai")
    print(f"  {a} // {b} = {a // b}        <- // floor division (int)")
    print(f"  {a} % {b}  = {a % b}        <- % remainder (even/odd check)")
    print(f"  {a} ** 2 = {a ** 2}      <- power")

    print("\nComparison (hamesha True/False):")
    print(f"  {a} > {b}   = {a > b}")
    print(f"  {a} == {b}  = {a == b}")
    print(f"  {a} != {b}  = {a != b}")

    print("\nLogical:")
    print(f"  True and False = {True and False}")
    print(f"  True or False  = {True or False}")
    print(f"  not True       = {not True}")

    print("\nMembership & Identity:")
    print(f'  "a" in "apple"        = {"a" in "apple"}')
    print(f"  5 in [1, 2, 3]        = {5 in [1, 2, 3]}")

    # INTERVIEW TRAP: == vs is
    x = [1, 2, 3]
    y = [1, 2, 3]
    print(f"\n  x == y  = {x == y}   <- values same hain")
    print(f"  x is y  = {x is y}  <- memory me alag objects hain")
    print("  == value check karta hai, is memory address check karta hai")


# ==============================================================
# 3. CONDITIONS (if / elif / else)
# ==============================================================

def conditions_demo():
    print("\n--- 3. CONDITIONS ---")

    def grade_salary(salary):
        """Salary ko category me daalo — SQL ke CASE jaisa."""
        if salary >= 50000:
            return "High"
        elif salary >= 30000:
            return "Medium"
        else:
            return "Low"

    for s in [70000, 35000, 18000]:
        print(f"  Salary {s:>6} -> {grade_salary(s)}")

    # Ternary — ek line me if-else
    n = 7
    print(f"\n  {n} is {'Even' if n % 2 == 0 else 'Odd'}")


# ==============================================================
# 4. LOOPS
# ==============================================================

def loops_demo():
    print("\n--- 4. LOOPS ---")

    print("for loop (1 se 5):")
    for i in range(1, 6):
        print(f"    i = {i}")

    print("\nwhile loop (countdown):")
    count = 3
    while count > 0:
        print(f"    count = {count}")
        count -= 1

    print("\nbreak / continue:")
    for i in range(1, 8):
        if i == 3:
            continue          # 3 ko skip
        if i == 6:
            break             # 6 pe loop band
        print(f"    i = {i}")

    print("\nenumerate — index + value dono:")
    names = ["Noman", "Ali", "Sara"]
    for index, name in enumerate(names, start=1):
        print(f"    {index}. {name}")

    print("\nzip — do list saath me:")
    salaries = [30000, 45000, 52000]
    for name, sal in zip(names, salaries):
        print(f"    {name:<6} -> {sal}")

    # INTERVIEW: nested loop — pattern printing
    print("\nPattern (nested loop):")
    for i in range(1, 5):
        print("    " + "* " * i)


# ==============================================================
# 5. STRINGS
# ==============================================================

def strings_demo():
    print("\n--- 5. STRINGS ---")

    s = "Python Developer"

    print(f'  s              = "{s}"')
    print(f"  len(s)         = {len(s)}")
    print(f"  s.upper()      = {s.upper()}")
    print(f"  s.lower()      = {s.lower()}")
    print(f"  s.split()      = {s.split()}")
    print(f"  s.replace()    = {s.replace('Python', 'Django')}")
    print(f"  s.find('Dev')  = {s.find('Dev')}")
    print(f"  s.startswith() = {s.startswith('Py')}")
    print(f'  "-".join(...)  = {"-".join(["a", "b", "c"])}')
    print(f'  "  hi  ".strip() = "{"  hi  ".strip()}"')

    print("\nSlicing  [start:end:step]  (end exclusive hota hai):")
    print(f"  s[0:6]   = {s[0:6]}")
    print(f"  s[:6]    = {s[:6]}")
    print(f"  s[7:]    = {s[7:]}")
    print(f"  s[-9:]   = {s[-9:]}      <- peeche se")
    print(f"  s[::-1]  = {s[::-1]}   <- REVERSE (interview favourite)")

    # INTERVIEW: Palindrome
    def is_palindrome(text):
        clean = text.lower().replace(" ", "")
        return clean == clean[::-1]

    print(f"\n  is_palindrome('madam') = {is_palindrome('madam')}")
    print(f"  is_palindrome('hello') = {is_palindrome('hello')}")

    # INTERVIEW: Count vowels
    def count_vowels(text):
        return sum(1 for ch in text.lower() if ch in "aeiou")

    print(f"  count_vowels('Python Developer') = {count_vowels(s)}")

    # STRINGS IMMUTABLE HAIN
    # s[0] = "J"   -> ERROR! String badal nahi sakte, naya banana padta hai


# ==============================================================
# 6. LIST  (ordered, mutable, duplicates allowed)
# ==============================================================

def list_demo():
    print("\n--- 6. LIST ---")

    nums = [10, 20, 30, 40, 50]
    print(f"  nums = {nums}")

    nums.append(60)
    print(f"  append(60)      -> {nums}")
    nums.insert(0, 5)
    print(f"  insert(0, 5)    -> {nums}")
    nums.remove(30)
    print(f"  remove(30)      -> {nums}")
    popped = nums.pop()
    print(f"  pop()           -> {nums}   (nikala: {popped})")

    print(f"\n  len      = {len(nums)}")
    print(f"  max/min  = {max(nums)} / {min(nums)}")
    print(f"  sum      = {sum(nums)}")
    print(f"  sorted   = {sorted(nums)}")
    print(f"  reverse  = {sorted(nums, reverse=True)}")

    # LIST COMPREHENSION — Python ki superpower
    print("\nList Comprehension:")
    squares = [x ** 2 for x in range(1, 6)]
    print(f"  squares          = {squares}")
    evens = [x for x in range(1, 11) if x % 2 == 0]
    print(f"  evens            = {evens}")
    labels = ["High" if x > 40 else "Low" for x in [30, 50, 20, 60]]
    print(f"  with if-else     = {labels}")

    # INTERVIEW: duplicates hatao
    dupes = [1, 2, 2, 3, 3, 3, 4]
    print(f"\n  remove duplicates: {dupes} -> {list(set(dupes))}")

    # INTERVIEW TRAP: shallow copy
    a = [1, 2, 3]
    b = a            # SAME list — dono ek hi cheez point karte hain
    c = a.copy()     # NAYI list
    b.append(99)
    print(f"\n  a = {a}   <- b badla to a bhi badal gaya!")
    print(f"  c = {c}         <- copy safe rahi")


# ==============================================================
# 7. TUPLE  (ordered, IMMUTABLE)
# ==============================================================

def tuple_demo():
    print("\n--- 7. TUPLE ---")

    emp = ("Noman", 21, 30000)
    print(f"  emp       = {emp}")
    print(f"  emp[0]    = {emp[0]}")

    # Unpacking
    name, age, salary = emp
    print(f"  unpacked  -> name={name}, age={age}, salary={salary}")

    # emp[0] = "Ali"   -> ERROR! Tuple badal nahi sakta

    print("\n  Tuple kab use karein?")
    print("    - Data badalna nahi chahiye (coordinates, DB row, config)")
    print("    - List se FAST hai")
    print("    - Dict ki key ban sakta hai, list nahi ban sakti")


# ==============================================================
# 8. SET  (unordered, unique, mutable)
# ==============================================================

def set_demo():
    print("\n--- 8. SET ---")

    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7}

    print(f"  a = {a}")
    print(f"  b = {b}")
    print(f"  union        a | b = {a | b}")
    print(f"  intersection a & b = {a & b}")
    print(f"  difference   a - b = {a - b}")
    print(f"  symmetric    a ^ b = {a ^ b}")

    print("\n  Duplicates automatically hat jaate hain:")
    print(f"    set([1,1,2,2,3]) = {set([1, 1, 2, 2, 3])}")


# ==============================================================
# 9. DICTIONARY  (key-value) — SABSE ZYADA USE HOTA HAI
# ==============================================================

def dict_demo():
    print("\n--- 9. DICTIONARY ---")
    print("  JSON, API response, DB row — sab dict hi hote hain.")

    emp = {"id": 1, "name": "Noman", "salary": 30000, "dept": "IT"}
    print(f"\n  emp = {emp}")

    print(f'  emp["name"]          = {emp["name"]}')
    print(f'  emp.get("phone")     = {emp.get("phone")}      <- None, crash nahi')
    print(f'  emp.get("phone","NA")= {emp.get("phone", "NA")}        <- default value')
    print("  DHYAAN: emp['phone'] crash karega. .get() safe hai.")

    emp["city"] = "Hyderabad"       # naya add
    emp["salary"] = 35000           # update
    print(f"\n  after update: {emp}")

    print(f"\n  keys()   = {list(emp.keys())}")
    print(f"  values() = {list(emp.values())}")

    print("\n  Loop (items):")
    for k, v in emp.items():
        print(f"    {k:<7} : {v}")

    # NESTED DICT — API response aisa hi dikhta hai
    print("\n  Nested dict (real API jaisa):")
    company = {
        "name": "TechCorp",
        "employees": [
            {"name": "Noman", "salary": 30000},
            {"name": "Ali", "salary": 45000},
        ],
    }
    print(f"    company['employees'][1]['name'] = {company['employees'][1]['name']}")

    # DICT COMPREHENSION
    squares = {x: x ** 2 for x in range(1, 6)}
    print(f"\n  dict comprehension: {squares}")


# ==============================================================
# INTERVIEW QUESTIONS
# ==============================================================
INTERVIEW = """
Q1. List vs Tuple?
    List  -> mutable,   [], slow,  dict ki key nahi ban sakti
    Tuple -> immutable, (), fast,  dict ki key ban sakti hai

Q2. List vs Set?
    List -> ordered, duplicates allowed, index se access
    Set  -> unordered, unique only, index nahi hota, lookup bahut fast

Q3. == vs is?
    == value compare karta hai
    is memory address (identity) compare karta hai

Q4. Mutable vs Immutable?
    Mutable   -> list, dict, set          (badal sakte hain)
    Immutable -> int, float, str, tuple   (nahi badal sakte)

Q5. String reverse kaise?
    s[::-1]

Q6. Duplicates kaise hataye list se?
    list(set(my_list))     (order chahiye to: list(dict.fromkeys(my_list)))

Q7. is vs ==  wala trap kya hai?
    do alag list same values ke saath: == True, is False

Q8. Shallow vs Deep copy?
    b = a        -> same object
    b = a.copy() -> shallow (upar ka level naya, andar ka same)
    copy.deepcopy(a) -> poora naya
"""


# ==============================================================
# PRACTICE — khud likh! Solutions: exercises/solutions_step01.py
# ==============================================================
PRACTICE = """
1. User se number lo aur even/odd batao.
2. 1 se 100 tak ke even numbers ka sum nikalo.
3. String me vowels count karo.
4. List me se sabse bada number nikalo (max() use kiye bina).
5. Ek string palindrome hai ya nahi check karo.
6. Dict me employees ka data rakho, phir sabse zyada salary wala print karo.
7. Do list ko merge karke duplicates hatao.
8. Multiplication table print karo (nested loop se).
"""


if __name__ == "__main__":
    print("=" * 62)
    print("STEP 1 — PYTHON BASICS")
    print("=" * 62)

    variables_demo()
    operators_demo()
    conditions_demo()
    loops_demo()
    strings_demo()
    list_demo()
    tuple_demo()
    set_demo()
    dict_demo()

    print("\n" + "=" * 62)
    print("INTERVIEW QUESTIONS")
    print("=" * 62)
    print(INTERVIEW)

    print("=" * 62)
    print("PRACTICE — ab khud likho")
    print("=" * 62)
    print(PRACTICE)
