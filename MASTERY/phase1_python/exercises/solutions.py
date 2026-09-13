"""
================================================================
PHASE 1 — PRACTICE SOLUTIONS
================================================================
Chalao:  python3 phase1_python/exercises/solutions.py

⚠️  PEHLE KHUD TRY KARO. Phir yahan dekho.
    Dekh ke likhne se kuch nahi hota. Atak jao tabhi kholo.
================================================================
"""

import json
import re
from pathlib import Path

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)


# ================================================================
# STEP 1 — BASICS
# ================================================================

def s1_even_odd(number):
    """1. Even ya odd batao."""
    return "Even" if number % 2 == 0 else "Odd"


def s1_sum_evens(limit=100):
    """2. 1 se 100 tak even numbers ka sum."""
    return sum(x for x in range(1, limit + 1) if x % 2 == 0)


def s1_count_vowels(text):
    """3. Vowels count karo."""
    return sum(1 for ch in text.lower() if ch in "aeiou")


def s1_max_without_builtin(numbers):
    """4. max() bina sabse bada nikalo."""
    if not numbers:
        return None
    biggest = numbers[0]
    for n in numbers[1:]:
        if n > biggest:
            biggest = n
    return biggest


def s1_is_palindrome(text):
    """5. Palindrome check."""
    clean = "".join(ch.lower() for ch in text if ch.isalnum())
    return clean == clean[::-1]


def s1_highest_paid(employees):
    """6. Sabse zyada salary wala."""
    return max(employees, key=lambda e: e["salary"])


def s1_merge_unique(list1, list2):
    """7. Merge + duplicates hatao (order bacha ke)."""
    return list(dict.fromkeys(list1 + list2))


def s1_multiplication_table(n=5):
    """8. Multiplication table."""
    return [[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]


# ================================================================
# STEP 2 — FUNCTIONS
# ================================================================

def s2_add(a, b):
    """1."""
    return a + b


def s2_is_even(n):
    """2."""
    return n % 2 == 0


def s2_greet(name, greeting="Hello"):
    """3. Default argument."""
    return f"{greeting}, {name}!"


def s2_total(*numbers):
    """4. *args."""
    return sum(numbers)


def s2_max_min(numbers):
    """5. Do values return."""
    return max(numbers), min(numbers)


def s2_calculate_tax(salary):
    """6. Slab wise tax."""
    rate = 0.05 if salary < 30000 else 0.10
    return round(salary * rate, 2)


def s2_recursive_sum(n):
    """7. Recursion."""
    if n <= 0:
        return 0
    return n + s2_recursive_sum(n - 1)


def s2_sort_by_name(employees):
    """8. Lambda + sorted."""
    return sorted(employees, key=lambda e: e["name"])


def s2_count_words(sentence):
    """9. Word frequency."""
    counts = {}
    for word in sentence.lower().split():
        word = word.strip(".,!?;:")
        counts[word] = counts.get(word, 0) + 1
    return counts


def s2_apply_twice(func, value):
    """10. Higher-order function."""
    return func(func(value))


# ================================================================
# STEP 3 — OOP
# ================================================================

class Employee:
    """1. Classic interview question."""

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print(f"    {self.name} {self.salary}")

    def __str__(self):
        return f"{self.name} - {self.salary}"


class Student:
    """2. Marks se grade."""

    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return "A"
        if avg >= 75:
            return "B"
        if avg >= 60:
            return "C"
        if avg >= 40:
            return "D"
        return "F"


class BankAccount:
    """3. Encapsulation."""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            return "Amount positive hona chahiye"
        self.__balance += amount
        return f"Deposited {amount}. Balance: {self.__balance}"

    def withdraw(self, amount):
        if amount <= 0:
            return "Amount positive hona chahiye"
        if amount > self.__balance:
            return "Insufficient balance"
        self.__balance -= amount
        return f"Withdrew {amount}. Balance: {self.__balance}"


class Animal:
    """4. Inheritance + overriding."""

    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Some sound"


class Dog(Animal):
    def speak(self):
        return "Bhow Bhow"


class Cat(Animal):
    def speak(self):
        return "Meow"


from abc import ABC, abstractmethod    # noqa: E402


class Shape(ABC):
    """5. Abstraction."""

    @abstractmethod
    def area(self):
        pass

    def describe(self):
        return f"{type(self).__name__} ka area = {self.area()}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return round(3.14159 * self.radius ** 2, 2)


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


class Car:
    """6. __str__"""

    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class Money:
    """7. __add__"""

    def __init__(self, amount, currency="INR"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Alag currency add nahi kar sakte")
        return Money(self.amount + other.amount, self.currency)

    def __str__(self):
        return f"{self.currency} {self.amount:,}"


class Manager(Employee):
    """8. Inheritance + extra field."""

    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def __str__(self):
        return f"{self.name} - {self.salary} (Manager of {self.team_size})"


class Product:
    """9. @property validation."""

    def __init__(self, name, price):
        self.name = name
        self._price = None
        self.price = price          # setter chalega

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price negative nahi ho sakta")
        self._price = value

    @property
    def price_with_gst(self):
        return round(self._price * 1.18, 2)


class Book:
    """10. Library system."""

    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_issued = False

    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"{self.book_id}. {self.title} by {self.author} [{status}]"


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        self.books[book.book_id] = book

    def issue(self, book_id):
        book = self.books.get(book_id)
        if not book:
            return "Book nahi mili"
        if book.is_issued:
            return "Pehle se issued hai"
        book.is_issued = True
        return f"'{book.title}' issue ho gayi"

    def return_book(self, book_id):
        book = self.books.get(book_id)
        if not book:
            return "Book nahi mili"
        book.is_issued = False
        return f"'{book.title}' wapas aa gayi"

    def available(self):
        return [b for b in self.books.values() if not b.is_issued]


# ================================================================
# STEP 4 — EXCEPTIONS
# ================================================================

def s4_safe_int(value):
    """1."""
    try:
        return int(value), None
    except ValueError:
        return None, "Valid number daalo"


def s4_safe_divide(a, b):
    """2."""
    try:
        return a / b, None
    except ZeroDivisionError:
        return None, "Zero se divide nahi kar sakte"
    except TypeError:
        return None, "Numbers hone chahiye"


def s4_read_file(path):
    """3."""
    try:
        return Path(path).read_text(encoding="utf-8"), None
    except FileNotFoundError:
        return None, f"File nahi mili: {path}"
    except PermissionError:
        return None, "Permission nahi hai"


def s4_get_key(data, key):
    """4."""
    try:
        return data[key], None
    except KeyError:
        return None, f"Key '{key}' nahi mili"


class NegativeSalaryError(Exception):
    """5. Custom exception."""

    def __init__(self, salary):
        self.salary = salary
        super().__init__(f"Salary negative nahi ho sakti: {salary}")


def s4_set_salary(salary):
    if salary < 0:
        raise NegativeSalaryError(salary)
    return salary


def s4_validate_age(age):
    """6."""
    if not isinstance(age, int):
        raise TypeError("Age integer honi chahiye")
    if age < 18:
        raise ValueError(f"Age {age} — minimum 18 chahiye")
    return f"Age {age} OK"


def s4_with_finally(value):
    """7."""
    log = []
    try:
        log.append(f"Result: {100 / value}")
    except ZeroDivisionError:
        log.append("Zero division error")
    finally:
        log.append("Program end")
    return log


def s4_calculator(a, b, op):
    """8. Sab handle karo, crash mat hone do."""
    try:
        a, b = float(a), float(b)
        ops = {
            "+": lambda: a + b, "-": lambda: a - b,
            "*": lambda: a * b, "/": lambda: a / b,
        }
        if op not in ops:
            return f"Unknown operator: {op}"
        return ops[op]()
    except ZeroDivisionError:
        return "Zero se divide nahi kar sakte"
    except (ValueError, TypeError):
        return "Valid numbers daalo"


def s4_retry(func, attempts=3):
    """9. Retry logic."""
    for i in range(1, attempts + 1):
        try:
            return func(), i
        except Exception:
            if i == attempts:
                return None, i
    return None, attempts


# ================================================================
# STEP 5 — FILES + JSON
# ================================================================

def s5_write_employees(path):
    """1."""
    employees = ["Noman,30000,IT", "Ali,45000,HR", "Sara,52000,IT",
                 "Zoya,38000,Sales", "Imran,41000,HR"]
    Path(path).write_text("\n".join(employees) + "\n", encoding="utf-8")
    return len(employees)


def s5_read_lines(path):
    """2."""
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def s5_append_employee(path, line):
    """3."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def s5_write_csv(path):
    """4."""
    import csv
    rows = [
        {"id": 1, "name": "Noman", "salary": 30000},
        {"id": 2, "name": "Ali", "salary": 45000},
        {"id": 3, "name": "Sara", "salary": 52000},
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "name", "salary"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def s5_csv_stats(path):
    """5."""
    import csv
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    salaries = [int(r["salary"]) for r in rows]
    return {"count": len(salaries), "total": sum(salaries),
            "average": round(sum(salaries) / len(salaries), 2)}


def s5_write_json(path):
    """6."""
    data = {"company": "TechCorp", "employees": [
        {"id": 1, "name": "Noman", "salary": 30000, "skills": ["Python", "SQL"]},
        {"id": 2, "name": "Ali", "salary": 45000, "skills": ["Excel"]},
    ]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def s5_find_employee(path, name):
    """7."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return next((e for e in data["employees"] if e["name"] == name), None)


def s5_update_salary(path, name, new_salary):
    """8. load -> modify -> dump"""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for e in data["employees"]:
        if e["name"] == name:
            e["salary"] = new_salary
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return True


def s5_delete_employee(path, emp_id):
    """9."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    before = len(data["employees"])
    data["employees"] = [e for e in data["employees"] if e["id"] != emp_id]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return before - len(data["employees"])


def s5_csv_to_json(csv_path, json_path):
    """11."""
    import csv
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4)
    return len(rows)


# ================================================================
# STEP 7 — LIBRARIES
# ================================================================

def s7_list_py_files(folder):
    """1."""
    return sorted(p.name for p in Path(folder).glob("*.py"))


def s7_date_formats():
    """2."""
    from datetime import datetime
    now = datetime.now()
    return {
        "db":     now.strftime("%Y-%m-%d"),
        "indian": now.strftime("%d/%m/%Y"),
        "full":   now.strftime("%d %B %Y"),
    }


def s7_calculate_age(birth_year, birth_month, birth_day):
    """3."""
    from datetime import date
    today = date.today()
    return today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))


EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]{2,}$")
PHONE_RE = re.compile(r"^[6-9]\d{9}$")


def s7_is_valid_email(email):
    """4."""
    return bool(EMAIL_RE.match(email))


def s7_is_valid_phone(phone):
    """5."""
    return bool(PHONE_RE.match(phone))


def s7_extract_emails(text):
    """6."""
    return re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)


def s7_folder_report(folder):
    """11."""
    return [(p.name, p.stat().st_size)
            for p in sorted(Path(folder).iterdir()) if p.is_file()]


# ================================================================
# DEMO — sab solutions chala ke dikhao
# ================================================================

def run_all():
    print("=" * 66)
    print("PHASE 1 — SOLUTIONS")
    print("=" * 66)

    # ---- STEP 1 ----
    print("\n[STEP 1 — BASICS]")
    print(f"  1. even_odd(7)              = {s1_even_odd(7)}")
    print(f"  2. sum_evens(100)           = {s1_sum_evens()}")
    print(f"  3. count_vowels('Python')   = {s1_count_vowels('Python Developer')}")
    print(f"  4. max([3,9,2,7])           = {s1_max_without_builtin([3, 9, 2, 7])}")
    print(f"  5. is_palindrome('madam')   = {s1_is_palindrome('madam')}")
    emps = [{"name": "Noman", "salary": 30000}, {"name": "Ali", "salary": 52000}]
    print(f"  6. highest_paid             = {s1_highest_paid(emps)}")
    print(f"  7. merge_unique             = {s1_merge_unique([1,2,3], [3,4,5])}")
    print(f"  8. multiplication_table(3)  = {s1_multiplication_table(3)}")

    # ---- STEP 2 ----
    print("\n[STEP 2 — FUNCTIONS]")
    print(f"  1. add(3, 7)                = {s2_add(3, 7)}")
    print(f"  2. is_even(10)              = {s2_is_even(10)}")
    print(f"  3. greet('Noman')           = {s2_greet('Noman')}")
    print(f"  4. total(1,2,3,4,5)         = {s2_total(1, 2, 3, 4, 5)}")
    print(f"  5. max_min([4,9,1])         = {s2_max_min([4, 9, 1])}")
    print(f"  6. calculate_tax(50000)     = {s2_calculate_tax(50000)}")
    print(f"  7. recursive_sum(10)        = {s2_recursive_sum(10)}")
    print(f"  8. sort_by_name             = {[e['name'] for e in s2_sort_by_name(emps)]}")
    print(f"  9. count_words              = {s2_count_words('the cat and the dog')}")
    print(f" 10. apply_twice(sq, 3)       = {s2_apply_twice(lambda x: x**2, 3)}")

    # ---- STEP 3 ----
    print("\n[STEP 3 — OOP]")
    print("  1. Employee:")
    Employee("Noman", 30000).display()
    st = Student("Sara", [85, 92, 78])
    print(f"  2. Student: avg={st.average():.1f}, grade={st.grade()}")
    acc = BankAccount("Noman", 10000)
    print(f"  3. {acc.deposit(5000)}")
    print(f"     {acc.withdraw(99999)}")
    print(f"  4. Dog: {Dog('Tommy').speak()},  Cat: {Cat('Kitty').speak()}")
    print(f"  5. {Circle(5).describe()}")
    print(f"     {Rectangle(4, 6).describe()}")
    print(f"  6. Car: {Car('Maruti', 'Swift', 2024)}")
    print(f"  7. Money: {Money(30000)} + {Money(5000)} = {Money(30000) + Money(5000)}")
    print(f"  8. Manager: {Manager('Sara', 80000, 5)}")
    p = Product("Laptop", 50000)
    print(f"  9. Product: price={p.price}, with GST={p.price_with_gst}")
    lib = Library()
    lib.add_book(Book(1, "Python Crash Course", "Eric Matthes"))
    lib.add_book(Book(2, "Clean Code", "Robert Martin"))
    print(f" 10. {lib.issue(1)}")
    print(f"     Available: {[b.title for b in lib.available()]}")

    # ---- STEP 4 ----
    print("\n[STEP 4 — EXCEPTIONS]")
    print(f"  1. safe_int('abc')          = {s4_safe_int('abc')}")
    print(f"  2. safe_divide(10, 0)       = {s4_safe_divide(10, 0)}")
    print(f"  3. read_file('nope.txt')    = {s4_read_file('nope.txt')}")
    print(f"  4. get_key({{'a':1}}, 'b')    = {s4_get_key({'a': 1}, 'b')}")
    try:
        s4_set_salary(-500)
    except NegativeSalaryError as e:
        print(f"  5. NegativeSalaryError      = {e}")
    try:
        s4_validate_age(15)
    except ValueError as e:
        print(f"  6. validate_age(15)         = {e}")
    print(f"  7. with_finally(0)          = {s4_with_finally(0)}")
    print(f"  8. calculator(10, 0, '/')   = {s4_calculator(10, 0, '/')}")
    print(f"     calculator(10, 5, '*')   = {s4_calculator(10, 5, '*')}")

    counter = {"n": 0}

    def flaky():
        counter["n"] += 1
        if counter["n"] < 3:
            raise ConnectionError("fail")
        return "Success"

    print(f"  9. retry(flaky)             = {s4_retry(flaky)}")

    # ---- STEP 5 ----
    print("\n[STEP 5 — FILES + JSON]")
    txt = OUT / "employees.txt"
    csvf = OUT / "employees.csv"
    jsonf = OUT / "employees.json"
    out_json = OUT / "from_csv.json"

    print(f"  1. write_employees          = {s5_write_employees(txt)} lines")
    print(f"  2. read_lines               = {len(s5_read_lines(txt))} lines")
    s5_append_employee(txt, "Rahul,35000,IT")
    print(f"  3. append                   = {len(s5_read_lines(txt))} lines ab")
    print(f"  4. write_csv                = {s5_write_csv(csvf)} rows")
    print(f"  5. csv_stats                = {s5_csv_stats(csvf)}")
    s5_write_json(jsonf)
    print(f"  6. write_json               = done")
    print(f"  7. find_employee('Ali')     = {s5_find_employee(jsonf, 'Ali')}")
    s5_update_salary(jsonf, "Noman", 35000)
    print(f"  8. update_salary            = {s5_find_employee(jsonf, 'Noman')['salary']}")
    print(f"  9. delete_employee(2)       = {s5_delete_employee(jsonf, 2)} deleted")
    print(f" 11. csv_to_json              = {s5_csv_to_json(csvf, out_json)} rows")

    # ---- STEP 7 ----
    print("\n[STEP 7 — LIBRARIES]")
    print(f"  1. py_files                 = {s7_list_py_files(Path(__file__).parent)}")
    print(f"  2. date_formats             = {s7_date_formats()}")
    print(f"  3. calculate_age(2005,3,15) = {s7_calculate_age(2005, 3, 15)}")
    print(f"  4. valid_email('a@b.com')   = {s7_is_valid_email('a@b.com')}")
    print(f"     valid_email('bad')       = {s7_is_valid_email('bad')}")
    print(f"  5. valid_phone('9876543210')= {s7_is_valid_phone('9876543210')}")
    print(f"     valid_phone('1234567890')= {s7_is_valid_phone('1234567890')}")
    text = "Contact noman@test.com or admin@corp.co.in"
    print(f"  6. extract_emails           = {s7_extract_emails(text)}")

    print("\n" + "=" * 66)
    print(f"Output files: {OUT}")
    print("=" * 66)


if __name__ == "__main__":
    run_all()
