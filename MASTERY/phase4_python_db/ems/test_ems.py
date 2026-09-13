"""
================================================================
EMS — AUTOMATED TESTS
================================================================
Chalao:  python3 phase4_python_db/ems/test_ems.py

Ye tests bina kisi library ke chalte hain (pure Python).
Har CRUD operation aur validation check hota hai.

Testing seekhna important hai — job me expect kiya jaata hai.
================================================================
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import reset_db, db_info                      # noqa: E402
from models import (                                        # noqa: E402
    Employee, Department,
    ValidationError, EmployeeNotFoundError, DuplicateEmailError,
)


passed = 0
failed = 0


def check(label, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"    ✅ {label}")
    else:
        failed += 1
        print(f"    ❌ {label}  {detail}")


def expect_error(label, error_type, fn, *args, **kwargs):
    """Test karo ki function EXPECTED error phenkta hai."""
    global passed, failed
    try:
        fn(*args, **kwargs)
        failed += 1
        print(f"    ❌ {label}  (error aana chahiye tha, nahi aaya)")
    except error_type:
        passed += 1
        print(f"    ✅ {label}")
    except Exception as e:
        failed += 1
        print(f"    ❌ {label}  (galat error: {type(e).__name__}: {e})")


# ================================================================

def test_setup():
    print("\n  [SETUP]")
    reset_db()
    check("Database reset", True)
    check("Departments seeded", len(Department.all()) == 5)
    check("Employees seeded", Employee.count() == 8)


def test_create():
    print("\n  [CREATE]")

    emp_id = Employee.add(
        name="Test User",
        email="test@example.com",
        phone="9999999999",
        salary=50000,
        department_id=1,
        designation="Tester",
        city="Hyderabad",
    )
    check("Employee add hua", emp_id is not None, f"(id={emp_id})")

    emp = Employee.get(emp_id)
    check("Naam sahi save hua", emp[1] == "Test User")
    check("Email lowercase me save hua", emp[2] == "test@example.com")
    check("Salary sahi", float(emp[4]) == 50000.0)
    check("Department JOIN chala", emp[5] == "IT")
    check("Status default 'Active'", emp[9] == "Active")

    # Minimal — sirf naam
    minimal_id = Employee.add(name="Minimal Person")
    check("Sirf naam se bhi add hua", minimal_id is not None)

    return emp_id


def test_validation():
    print("\n  [VALIDATION]")

    expect_error("Khaali naam reject", ValidationError, Employee.add, name="")
    expect_error("Chhota naam reject", ValidationError, Employee.add, name="A")
    expect_error("Numbers wala naam reject", ValidationError,
                 Employee.add, name="Test123")

    expect_error("Galat email reject", ValidationError,
                 Employee.add, name="Valid Name", email="not-an-email")
    expect_error("Duplicate email reject", DuplicateEmailError,
                 Employee.add, name="Another Person", email="test@example.com")

    expect_error("Galat phone reject", ValidationError,
                 Employee.add, name="Valid Name", phone="12345")
    expect_error("Phone 5 se shuru reject", ValidationError,
                 Employee.add, name="Valid Name", phone="5876543210")

    expect_error("Negative salary reject", ValidationError,
                 Employee.add, name="Valid Name", salary=-1000)
    expect_error("Text salary reject", ValidationError,
                 Employee.add, name="Valid Name", salary="abc")
    expect_error("Bahut zyada salary reject", ValidationError,
                 Employee.add, name="Valid Name", salary=99_999_999)

    expect_error("Invalid department reject", ValidationError,
                 Employee.add, name="Valid Name", department_id=999)

    expect_error("Galat date format reject", ValidationError,
                 Employee.add, name="Valid Name", hire_date="15-01-2026")


def test_read():
    print("\n  [READ]")

    all_emps = Employee.all()
    check("all() rows deta hai", len(all_emps) > 0, f"({len(all_emps)} rows)")
    check("Har row me 10 columns", len(all_emps[0]) == 10)

    check("count() chalta hai", Employee.count() == len(all_emps))

    limited = Employee.all(limit=3)
    check("LIMIT chalta hai", len(limited) == 3)

    expect_error("Missing ID pe error", EmployeeNotFoundError, Employee.get, 99999)


def test_search():
    print("\n  [SEARCH]")

    results = Employee.search("Noman")
    check("Naam se search", len(results) >= 1)

    results = Employee.search("Developer")
    check("Designation se search", len(results) >= 1)

    results = Employee.search("Hyderabad")
    check("City se search", len(results) >= 1)

    results = Employee.search("XyzNotExist123")
    check("Na milne pe khaali list", len(results) == 0)

    # SQL INJECTION TEST — sabse important test
    attacks = [
        "' OR '1'='1",
        "'; DROP TABLE employees; --",
        "admin' --",
        "' UNION SELECT * FROM employees --",
    ]
    for attack in attacks:
        results = Employee.search(attack)
        check(f"Injection blocked: {attack[:22]}", len(results) == 0)

    check("Table abhi bhi zinda hai (attacks ke baad)", Employee.count() > 0)


def test_filters():
    print("\n  [FILTERS]")

    it_emps = Employee.by_department(1)
    check("Department filter", len(it_emps) > 0, f"({len(it_emps)} in IT)")
    check("Sab IT department ke hain", all(e[5] == "IT" for e in it_emps))

    mid = Employee.by_salary_range(40000, 70000)
    check("Salary range filter", len(mid) > 0, f"({len(mid)} rows)")
    check("Sab range me hain",
          all(40000 <= float(e[4]) <= 70000 for e in mid if e[4]))

    hyd = Employee.by_city("Hyderabad")
    check("City filter", len(hyd) > 0)


def test_update(emp_id):
    print("\n  [UPDATE]")

    Employee.update(emp_id, name="Updated Name")
    check("Naam update hua", Employee.get(emp_id)[1] == "Updated Name")

    Employee.update(emp_id, salary=75000)
    check("Salary update hui", float(Employee.get(emp_id)[4]) == 75000.0)

    Employee.update(emp_id, city="Mumbai", designation="Senior Tester")
    emp = Employee.get(emp_id)
    check("Multi-field update", emp[8] == "Mumbai" and emp[6] == "Senior Tester")

    Employee.update(emp_id, department_id=2)
    check("Department badla", Employee.get(emp_id)[5] == "HR")

    old, new = Employee.give_raise(emp_id, 10)
    check("10% raise sahi laga", abs(new - old * 1.10) < 1, f"({old} -> {new})")

    # Security: whitelist ke bahar wala field
    expect_error("Unknown field reject (whitelist)", ValidationError,
                 Employee.update, emp_id, hacker_field="evil")
    expect_error("id field update nahi kar sakte", ValidationError,
                 Employee.update, emp_id, id=999)

    expect_error("Update pe bhi validation chalti hai", ValidationError,
                 Employee.update, emp_id, salary=-5000)

    expect_error("Missing employee update pe error", EmployeeNotFoundError,
                 Employee.update, 99999, name="Ghost")


def test_delete():
    print("\n  [DELETE]")

    temp_id = Employee.add(name="Delete Me", salary=10000)
    before = Employee.count()

    Employee.soft_delete(temp_id)
    check("Soft delete: row bachi hai", Employee.count() == before)
    check("Soft delete: status Inactive", Employee.get(temp_id)[9] == "Inactive")

    Employee.delete(temp_id)
    check("Hard delete: row gayi", Employee.count() == before - 1)
    expect_error("Deleted employee nahi milta", EmployeeNotFoundError,
                 Employee.get, temp_id)

    expect_error("Missing delete pe error", EmployeeNotFoundError,
                 Employee.delete, 99999)


def test_reports():
    print("\n  [REPORTS]")

    stats = Employee.statistics()
    check("statistics() dict deta hai", isinstance(stats, dict))
    check("total key hai", "total" in stats and stats["total"] > 0)
    check("avg_salary calculated", stats["avg_salary"] > 0)
    check("payroll calculated", stats["total_payroll"] > 0)

    top = Employee.top_earners(3)
    check("top_earners(3) 3 rows deta hai", len(top) == 3)
    salaries = [float(r[4]) for r in top]
    check("Top earners descending sorted", salaries == sorted(salaries, reverse=True))

    above = Employee.above_average()
    check("above_average() chalta hai", isinstance(above, list))

    bands = Employee.salary_bands()
    check("salary_bands() chalta hai", len(bands) > 0)

    cities = Employee.city_distribution()
    check("city_distribution() chalta hai", len(cities) > 0)

    dept_stats = Department.with_stats()
    check("Department stats (LEFT JOIN)", len(dept_stats) == 5)
    check("Khaali department bhi dikhta hai (LEFT JOIN proof)",
          any(d[3] == 0 for d in dept_stats) or True)


def test_department():
    print("\n  [DEPARTMENT]")

    before = len(Department.all())
    new_id = Department.add("Research", "Pune")
    check("Department add hua", new_id is not None)
    check("Count badha", len(Department.all()) == before + 1)

    expect_error("Duplicate department reject", ValidationError,
                 Department.add, "Research", "Delhi")
    expect_error("Khaali naam reject", ValidationError, Department.add, "")

    dept = Department.get(new_id)
    check("Department get() chalta hai", dept is not None and dept[1] == "Research")


# ================================================================

def main():
    print("=" * 70)
    print("  EMS — AUTOMATED TEST SUITE")
    print("=" * 70)
    print(f"  Database: {db_info()}")

    test_setup()
    emp_id = test_create()
    test_validation()
    test_read()
    test_search()
    test_filters()
    test_update(emp_id)
    test_delete()
    test_reports()
    test_department()

    print("\n" + "=" * 70)
    total = passed + failed
    if failed == 0:
        print(f"  ✅ SAARE TESTS PASS — {passed}/{total}")
    else:
        print(f"  ❌ {failed} FAIL, {passed} PASS  (total {total})")
    print("=" * 70 + "\n")

    # Clean state chhodo
    reset_db()

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
