"""
================================================================
EMS — MODELS (Business Logic + CRUD)
================================================================
Ye layer database ke saath baat karti hai.

DHYAAN DO:
  - Har query PARAMETERIZED hai (? placeholder) — SQL injection safe
  - Validation model me hai, UI me nahi
  - UI (main.py) ko SQL ka kuch nahi pata

Ye exactly wahi structure hai jo Django me models.py hota hai.
Isliye ye project Django ki seedhi tayyari hai.
================================================================
"""

import re
from datetime import date

from database import fetch_all, fetch_one, execute, execute_returning_id


# ================================================================
# CUSTOM EXCEPTIONS (Step 4 ka use)
# ================================================================

class EmployeeError(Exception):
    """Base exception — saare employee errors ka parent."""


class ValidationError(EmployeeError):
    """Input galat hai."""


class EmployeeNotFoundError(EmployeeError):
    def __init__(self, emp_id):
        self.emp_id = emp_id
        super().__init__(f"Employee ID {emp_id} nahi mila")


class DuplicateEmailError(EmployeeError):
    def __init__(self, email):
        super().__init__(f"Email '{email}' pehle se registered hai")


# ================================================================
# VALIDATORS (Step 7 ka regex use)
# ================================================================

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]{2,}$")
PHONE_RE = re.compile(r"^[6-9]\d{9}$")


def validate_name(name):
    name = (name or "").strip()
    if len(name) < 2:
        raise ValidationError("Naam kam se kam 2 character ka hona chahiye")
    if len(name) > 100:
        raise ValidationError("Naam 100 character se zyada nahi")
    if not re.match(r"^[A-Za-z\s.'-]+$", name):
        raise ValidationError("Naam me sirf letters allowed hain")
    return name


def validate_email(email, exclude_id=None):
    email = (email or "").strip().lower()
    if not email:
        return None                      # email optional hai
    if not EMAIL_RE.match(email):
        raise ValidationError(f"Email format galat hai: {email}")

    # Duplicate check
    if exclude_id:
        row = fetch_one(
            "SELECT id FROM employees WHERE email = ? AND id != ?", (email, exclude_id))
    else:
        row = fetch_one("SELECT id FROM employees WHERE email = ?", (email,))
    if row:
        raise DuplicateEmailError(email)
    return email


def validate_phone(phone):
    phone = (phone or "").strip()
    if not phone:
        return None
    if not PHONE_RE.match(phone):
        raise ValidationError("Phone 10 digit ka ho aur 6-9 se shuru ho")
    return phone


def validate_salary(salary):
    if salary in (None, ""):
        return None
    try:
        salary = float(salary)
    except (TypeError, ValueError):
        raise ValidationError("Salary number honi chahiye")
    if salary < 0:
        raise ValidationError("Salary negative nahi ho sakti")
    if salary > 10_000_000:
        raise ValidationError("Salary bahut zyada hai — dobara check karo")
    return salary


def validate_department(dept_id):
    if dept_id in (None, ""):
        return None
    try:
        dept_id = int(dept_id)
    except (TypeError, ValueError):
        raise ValidationError("Department ID number honi chahiye")
    if not fetch_one("SELECT id FROM departments WHERE id = ?", (dept_id,)):
        raise ValidationError(f"Department ID {dept_id} exist nahi karta")
    return dept_id


def validate_date(value):
    value = (value or "").strip()
    if not value:
        return date.today().isoformat()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        raise ValidationError("Date format: YYYY-MM-DD hona chahiye")
    return value


# ================================================================
# DEPARTMENT
# ================================================================

class Department:

    @staticmethod
    def all():
        return fetch_all(
            "SELECT id, department_name, location FROM departments ORDER BY id")

    @staticmethod
    def get(dept_id):
        return fetch_one(
            "SELECT id, department_name, location FROM departments WHERE id = ?",
            (dept_id,))

    @staticmethod
    def add(name, location=None):
        name = (name or "").strip()
        if not name:
            raise ValidationError("Department ka naam chahiye")
        if fetch_one("SELECT id FROM departments WHERE department_name = ?", (name,)):
            raise ValidationError(f"Department '{name}' pehle se hai")
        return execute_returning_id(
            "INSERT INTO departments (department_name, location) VALUES (?, ?)",
            (name, location))

    @staticmethod
    def with_stats():
        """Har department ka summary — LEFT JOIN + GROUP BY (Step 11+12)."""
        return fetch_all("""
            SELECT
                d.id,
                d.department_name,
                d.location,
                COUNT(e.id)                                AS headcount,
                COALESCE(ROUND(AVG(e.salary)), 0)          AS avg_salary,
                COALESCE(SUM(e.salary), 0)                 AS total_cost
            FROM departments d
            LEFT JOIN employees e
                   ON d.id = e.department_id AND e.status = 'Active'
            GROUP BY d.id, d.department_name, d.location
            ORDER BY headcount DESC
        """)


# ================================================================
# EMPLOYEE — poora CRUD
# ================================================================

BASE_SELECT = """
    SELECT
        e.id, e.name, e.email, e.phone, e.salary,
        d.department_name, e.designation, e.hire_date, e.city, e.status
    FROM employees e
    LEFT JOIN departments d ON e.department_id = d.id
"""


class Employee:

    # ---------------- CREATE ----------------
    @staticmethod
    def add(name, email=None, phone=None, salary=None, department_id=None,
            designation=None, hire_date=None, city=None):
        """Naya employee add karo. Validation pehle, insert baad me."""
        name          = validate_name(name)
        email         = validate_email(email)
        phone         = validate_phone(phone)
        salary        = validate_salary(salary)
        department_id = validate_department(department_id)
        hire_date     = validate_date(hire_date)

        return execute_returning_id("""
            INSERT INTO employees
                (name, email, phone, salary, department_id,
                 designation, hire_date, city, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Active')
        """, (name, email, phone, salary, department_id,
              designation, hire_date, city))

    # ---------------- READ ----------------
    @staticmethod
    def all(limit=None, offset=0):
        sql = BASE_SELECT + " ORDER BY e.id"
        if limit:
            sql += f" LIMIT {int(limit)} OFFSET {int(offset)}"
        return fetch_all(sql)

    @staticmethod
    def get(emp_id):
        row = fetch_one(BASE_SELECT + " WHERE e.id = ?", (emp_id,))
        if not row:
            raise EmployeeNotFoundError(emp_id)
        return row

    @staticmethod
    def count():
        return fetch_one("SELECT COUNT(*) FROM employees")[0]

    # ---------------- SEARCH ----------------
    @staticmethod
    def search(keyword):
        """
        Naam / email / designation / city me dhoondho.

        ⚠️ DHYAAN: '%' VALUE me hai, query string me NAHI.
           Isliye ye SQL injection safe hai.
        """
        pattern = f"%{keyword}%"
        return fetch_all(BASE_SELECT + """
            WHERE e.name LIKE ?
               OR e.email LIKE ?
               OR e.designation LIKE ?
               OR e.city LIKE ?
            ORDER BY e.name
        """, (pattern, pattern, pattern, pattern))

    @staticmethod
    def by_department(dept_id):
        return fetch_all(
            BASE_SELECT + " WHERE e.department_id = ? ORDER BY e.salary DESC",
            (dept_id,))

    @staticmethod
    def by_salary_range(min_salary=0, max_salary=99_999_999):
        return fetch_all(
            BASE_SELECT + " WHERE e.salary BETWEEN ? AND ? ORDER BY e.salary DESC",
            (min_salary, max_salary))

    @staticmethod
    def by_city(city):
        return fetch_all(
            BASE_SELECT + " WHERE e.city = ? ORDER BY e.name", (city,))

    # ---------------- UPDATE ----------------
    @staticmethod
    def update(emp_id, **fields):
        """
        Jo fields diye gaye sirf wo update honge (partial update).

        DYNAMIC QUERY BUILDING:
          Column names WHITELIST se aate hain (user input se nahi)
          Values placeholder se jaati hain
          -> SQL injection safe
        """
        Employee.get(emp_id)      # exist karta hai? nahi to exception

        allowed = {
            "name": validate_name,
            "email": lambda v: validate_email(v, exclude_id=emp_id),
            "phone": validate_phone,
            "salary": validate_salary,
            "department_id": validate_department,
            "hire_date": validate_date,
            "designation": lambda v: (v or "").strip() or None,
            "city": lambda v: (v or "").strip() or None,
            "status": lambda v: v if v in ("Active", "Inactive") else "Active",
        }

        updates, values = [], []
        for key, value in fields.items():
            if key not in allowed:              # ⬅️ WHITELIST — ye zaroori hai
                raise ValidationError(f"'{key}' update nahi kar sakte")
            clean = allowed[key](value)
            updates.append(f"{key} = ?")
            values.append(clean)

        if not updates:
            raise ValidationError("Update karne ke liye kuch diya hi nahi")

        values.append(emp_id)
        sql = f"UPDATE employees SET {', '.join(updates)} WHERE id = ?"
        return execute(sql, tuple(values))

    @staticmethod
    def give_raise(emp_id, percent):
        """Percentage raise do."""
        emp = Employee.get(emp_id)
        if emp[4] is None:
            raise ValidationError("Is employee ki salary set hi nahi hai")
        try:
            percent = float(percent)
        except (TypeError, ValueError):
            raise ValidationError("Percent number hona chahiye")
        if not -100 < percent <= 200:
            raise ValidationError("Percent -100 se 200 ke beech ho")

        new_salary = round(float(emp[4]) * (1 + percent / 100), 2)
        execute("UPDATE employees SET salary = ? WHERE id = ?", (new_salary, emp_id))
        return float(emp[4]), new_salary

    # ---------------- DELETE ----------------
    @staticmethod
    def delete(emp_id):
        Employee.get(emp_id)      # exist check
        return execute("DELETE FROM employees WHERE id = ?", (emp_id,))

    @staticmethod
    def soft_delete(emp_id):
        """
        Row delete karne ki jagah status 'Inactive' kar do.

        REAL PROJECTS ME YEHI HOTA HAI —
        data kabhi sach me delete nahi karte (audit, recovery).
        Django me bhi is pattern ko soft delete kehte hain.
        """
        Employee.get(emp_id)
        return execute("UPDATE employees SET status = 'Inactive' WHERE id = ?", (emp_id,))

    # ---------------- REPORTS ----------------
    @staticmethod
    def statistics():
        row = fetch_one("""
            SELECT
                COUNT(*)                          AS total,
                COUNT(salary)                     AS with_salary,
                COALESCE(ROUND(AVG(salary)), 0)   AS avg_salary,
                COALESCE(MAX(salary), 0)          AS max_salary,
                COALESCE(MIN(salary), 0)          AS min_salary,
                COALESCE(SUM(salary), 0)          AS total_payroll
            FROM employees WHERE status = 'Active'
        """)
        return {
            "total": row[0], "with_salary": row[1], "avg_salary": row[2],
            "max_salary": row[3], "min_salary": row[4], "total_payroll": row[5],
        }

    @staticmethod
    def top_earners(n=5):
        return fetch_all(
            BASE_SELECT + """
            WHERE e.salary IS NOT NULL AND e.status = 'Active'
            ORDER BY e.salary DESC LIMIT ?""", (n,))

    @staticmethod
    def above_average():
        """Subquery ka use (Step 14)."""
        return fetch_all(BASE_SELECT + """
            WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE salary IS NOT NULL)
            ORDER BY e.salary DESC
        """)

    @staticmethod
    def salary_bands():
        """CASE ka use (Step 13)."""
        return fetch_all("""
            SELECT
                CASE
                    WHEN salary IS NULL   THEN 'Not Set'
                    WHEN salary >= 80000  THEN 'A (80k+)'
                    WHEN salary >= 60000  THEN 'B (60-80k)'
                    WHEN salary >= 40000  THEN 'C (40-60k)'
                    ELSE 'D (<40k)'
                END AS band,
                COUNT(*)                        AS employees,
                COALESCE(ROUND(AVG(salary)), 0) AS avg_salary
            FROM employees
            WHERE status = 'Active'
            GROUP BY band
            ORDER BY avg_salary DESC
        """)

    @staticmethod
    def city_distribution():
        return fetch_all("""
            SELECT city, COUNT(*) AS count, COALESCE(ROUND(AVG(salary)), 0) AS avg_salary
            FROM employees
            WHERE city IS NOT NULL AND status = 'Active'
            GROUP BY city
            ORDER BY count DESC
        """)
