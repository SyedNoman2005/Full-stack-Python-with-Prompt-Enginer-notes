"""
================================================================
EMPLOYEE MANAGEMENT SYSTEM  🏆
================================================================
Chalao:  python3 phase4_python_db/ems/main.py

FEATURES (tere list ke hisaab se):
   1. Add employee
   2. View employees
   3. Search employee
   4. Update employee
   5. Delete employee
   6. Search by department
   7. Salary filtering
   + Reports / Statistics

YE PROJECT SAB KUCH USE KARTA HAI:
  Step 1  Basics        -> loops, conditions, dict
  Step 2  Functions     -> har feature ek function
  Step 3  OOP           -> Employee, Department classes
  Step 4  Exceptions    -> custom exceptions + validation
  Step 5  Files         -> CSV export
  Step 6  Modules       -> config, database, models alag files
  Step 7  Libraries     -> re (validation), datetime
  Step 9-17 SQL         -> CRUD, JOIN, GROUP BY, CASE, subquery, transactions

IS PROJECT KO KHUD SE DOBARA LIKHNA = FOUNDATION COMPLETE.
================================================================
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

# Is folder ko import path me daalo
sys.path.insert(0, str(Path(__file__).parent))

from config import APP_NAME, APP_VERSION                    # noqa: E402
from database import init_db, db_info, reset_db             # noqa: E402
from models import (                                        # noqa: E402
    Employee, Department,
    EmployeeError, ValidationError, EmployeeNotFoundError, DuplicateEmailError,
)


# ================================================================
# DISPLAY HELPERS
# ================================================================

def header(title):
    print("\n" + "=" * 78)
    print(f"  {title}")
    print("=" * 78)


def money(value):
    if value is None:
        return "-"
    return f"{float(value):,.0f}"


def show_employees(rows, title="EMPLOYEES"):
    """Employee list ko table format me dikhao."""
    header(title)

    if not rows:
        print("\n  Koi employee nahi mila.\n")
        return

    print(f"\n  {'ID':<4} {'NAME':<18} {'DEPARTMENT':<12} {'DESIGNATION':<20} "
          f"{'SALARY':>10}  {'CITY':<12} {'STATUS':<9}")
    print("  " + "-" * 92)

    for r in rows:
        emp_id, name, email, phone, salary, dept, desig, hire, city, status = r
        print(f"  {emp_id:<4} {(name or '')[:17]:<18} {(dept or '-')[:11]:<12} "
              f"{(desig or '-')[:19]:<20} {money(salary):>10}  "
              f"{(city or '-')[:11]:<12} {status:<9}")

    print("  " + "-" * 92)
    print(f"  Total: {len(rows)} employee(s)\n")


def show_employee_detail(row):
    emp_id, name, email, phone, salary, dept, desig, hire, city, status = row
    header(f"EMPLOYEE #{emp_id}")
    print(f"""
    Name        : {name}
    Email       : {email or '-'}
    Phone       : {phone or '-'}
    Salary      : {money(salary)}
    Annual      : {money(salary * 12) if salary else '-'}
    Department  : {dept or 'Not Assigned'}
    Designation : {desig or '-'}
    City        : {city or '-'}
    Hire Date   : {hire or '-'}
    Status      : {status}
    """)


def ask(prompt, default=None, required=False):
    """Input lo. Blank chhoda to default."""
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"  {prompt}{suffix}: ").strip()
        if not value and default is not None:
            return default
        if not value and required:
            print("    ⚠️  Ye field zaroori hai")
            continue
        return value or None


def pause():
    input("\n  Enter dabao continue karne ke liye...")


# ================================================================
# FEATURE 1 — ADD EMPLOYEE
# ================================================================

def add_employee():
    header("1. ADD EMPLOYEE")

    print("\n  Available Departments:")
    for d in Department.all():
        print(f"    {d[0]}. {d[1]:<12} ({d[2]})")
    print()

    try:
        name        = ask("Name", required=True)
        email       = ask("Email (optional)")
        phone       = ask("Phone (10 digit)")
        salary      = ask("Salary")
        dept_id     = ask("Department ID")
        designation = ask("Designation")
        city        = ask("City")
        hire_date   = ask("Hire Date (YYYY-MM-DD)", default=datetime.now().strftime("%Y-%m-%d"))

        emp_id = Employee.add(
            name=name, email=email, phone=phone, salary=salary,
            department_id=dept_id, designation=designation,
            hire_date=hire_date, city=city,
        )
        print(f"\n  ✅ Employee add ho gaya! ID = {emp_id}")
        show_employee_detail(Employee.get(emp_id))

    except (ValidationError, DuplicateEmailError) as e:
        print(f"\n  ❌ {type(e).__name__}: {e}")
    except EmployeeError as e:
        print(f"\n  ❌ Error: {e}")


# ================================================================
# FEATURE 2 — VIEW EMPLOYEES
# ================================================================

def view_employees():
    header("2. VIEW EMPLOYEES")
    print("""
    1. Sab employees
    2. Ek employee (ID se)
    3. Top earners
    4. Average se zyada kamane wale
    """)

    choice = ask("Choice", default="1")

    try:
        if choice == "1":
            show_employees(Employee.all(), "ALL EMPLOYEES")

        elif choice == "2":
            emp_id = ask("Employee ID", required=True)
            show_employee_detail(Employee.get(int(emp_id)))

        elif choice == "3":
            n = int(ask("Kitne top earners", default="5"))
            show_employees(Employee.top_earners(n), f"TOP {n} EARNERS")

        elif choice == "4":
            show_employees(Employee.above_average(), "ABOVE AVERAGE SALARY")

        else:
            print("\n  ⚠️  Galat choice")

    except EmployeeNotFoundError as e:
        print(f"\n  ❌ {e}")
    except ValueError:
        print("\n  ❌ Number daalo")


# ================================================================
# FEATURE 3 — SEARCH EMPLOYEE
# ================================================================

def search_employee():
    header("3. SEARCH EMPLOYEE")
    print("\n  Naam / email / designation / city me dhoondhega")

    keyword = ask("Search keyword", required=True)
    results = Employee.search(keyword)
    show_employees(results, f"SEARCH RESULTS: '{keyword}'")

    print("  💡 Ye query parameterized hai (LIKE ?) — SQL injection safe hai.")
    print("     Try karo: ' OR '1'='1   — kuch nahi hoga.\n")


# ================================================================
# FEATURE 4 — UPDATE EMPLOYEE
# ================================================================

def update_employee():
    header("4. UPDATE EMPLOYEE")

    try:
        emp_id = int(ask("Employee ID", required=True))
        current = Employee.get(emp_id)
        show_employee_detail(current)

        print("""
    1. Name          5. Designation
    2. Email         6. City
    3. Phone         7. Department
    4. Salary        8. Percentage raise do
        """)

        choice = ask("Kya update karna hai", required=True)

        field_map = {
            "1": "name", "2": "email", "3": "phone", "4": "salary",
            "5": "designation", "6": "city", "7": "department_id",
        }

        if choice == "8":
            percent = ask("Raise percentage (jaise 10)", required=True)
            old, new = Employee.give_raise(emp_id, percent)
            print(f"\n  ✅ Salary: {money(old)} -> {money(new)} ({percent}% raise)")

        elif choice in field_map:
            field = field_map[choice]
            if field == "department_id":
                print("\n  Departments:")
                for d in Department.all():
                    print(f"    {d[0]}. {d[1]}")
            value = ask(f"Nayi {field}", required=True)
            Employee.update(emp_id, **{field: value})
            print(f"\n  ✅ {field} update ho gaya")

        else:
            print("\n  ⚠️  Galat choice")
            return

        show_employee_detail(Employee.get(emp_id))

    except EmployeeNotFoundError as e:
        print(f"\n  ❌ {e}")
    except (ValidationError, DuplicateEmailError) as e:
        print(f"\n  ❌ {e}")
    except ValueError:
        print("\n  ❌ Valid number daalo")


# ================================================================
# FEATURE 5 — DELETE EMPLOYEE
# ================================================================

def delete_employee():
    header("5. DELETE EMPLOYEE")

    try:
        emp_id = int(ask("Employee ID", required=True))
        emp = Employee.get(emp_id)
        show_employee_detail(emp)

        print("""
    1. Soft delete  (status = Inactive)  <- REAL PROJECTS ME YEHI
    2. Hard delete  (row hamesha ke liye gayab)
    3. Cancel
        """)

        choice = ask("Choice", default="3")

        if choice == "1":
            Employee.soft_delete(emp_id)
            print(f"\n  ✅ Employee #{emp_id} Inactive kar diya (data safe hai)")

        elif choice == "2":
            confirm = ask(f"PAKKA delete karna hai #{emp_id}? (yes/no)", default="no")
            if confirm.lower() == "yes":
                Employee.delete(emp_id)
                print(f"\n  ✅ Employee #{emp_id} delete ho gaya")
            else:
                print("\n  Cancel kiya")
        else:
            print("\n  Cancel kiya")

    except EmployeeNotFoundError as e:
        print(f"\n  ❌ {e}")
    except ValueError:
        print("\n  ❌ Valid number daalo")


# ================================================================
# FEATURE 6 — SEARCH BY DEPARTMENT
# ================================================================

def search_by_department():
    header("6. SEARCH BY DEPARTMENT")

    print("\n  Departments (with stats):\n")
    print(f"  {'ID':<4} {'DEPARTMENT':<14} {'LOCATION':<12} {'COUNT':>6} "
          f"{'AVG SALARY':>12} {'TOTAL COST':>12}")
    print("  " + "-" * 66)
    for d in Department.with_stats():
        print(f"  {d[0]:<4} {d[1]:<14} {(d[2] or '-'):<12} {d[3]:>6} "
              f"{money(d[4]):>12} {money(d[5]):>12}")
    print("  " + "-" * 66)

    dept_id = ask("\n  Department ID (blank = skip)")
    if dept_id:
        try:
            dept = Department.get(int(dept_id))
            if not dept:
                print("\n  ❌ Department nahi mila")
                return
            show_employees(Employee.by_department(int(dept_id)),
                           f"DEPARTMENT: {dept[1]}")
        except ValueError:
            print("\n  ❌ Valid number daalo")


# ================================================================
# FEATURE 7 — SALARY FILTERING
# ================================================================

def salary_filtering():
    header("7. SALARY FILTERING")
    print("""
    1. Salary range (min - max)
    2. Salary bands report
    3. City-wise distribution
    """)

    choice = ask("Choice", default="1")

    try:
        if choice == "1":
            min_sal = float(ask("Minimum salary", default="0"))
            max_sal = float(ask("Maximum salary", default="99999999"))
            show_employees(
                Employee.by_salary_range(min_sal, max_sal),
                f"SALARY: {money(min_sal)} - {money(max_sal)}")

        elif choice == "2":
            header("SALARY BANDS")
            print(f"\n  {'BAND':<14} {'EMPLOYEES':>10} {'AVG SALARY':>14}")
            print("  " + "-" * 40)
            for band, count, avg in Employee.salary_bands():
                print(f"  {band:<14} {count:>10} {money(avg):>14}")
            print()

        elif choice == "3":
            header("CITY DISTRIBUTION")
            print(f"\n  {'CITY':<16} {'EMPLOYEES':>10} {'AVG SALARY':>14}")
            print("  " + "-" * 42)
            for city, count, avg in Employee.city_distribution():
                print(f"  {city:<16} {count:>10} {money(avg):>14}")
            print()

        else:
            print("\n  ⚠️  Galat choice")

    except ValueError:
        print("\n  ❌ Valid number daalo")


# ================================================================
# FEATURE 8 — STATISTICS DASHBOARD
# ================================================================

def statistics():
    header("8. STATISTICS DASHBOARD")

    s = Employee.statistics()
    print(f"""
    Total Active Employees : {s['total']}
    Salary Data Available  : {s['with_salary']}

    Average Salary         : {money(s['avg_salary'])}
    Highest Salary         : {money(s['max_salary'])}
    Lowest Salary          : {money(s['min_salary'])}

    Monthly Payroll        : {money(s['total_payroll'])}
    Annual Payroll         : {money(s['total_payroll'] * 12)}
    """)

    print("  " + "-" * 60)
    print("\n  DEPARTMENT BREAKDOWN:\n")
    print(f"  {'DEPARTMENT':<14} {'COUNT':>6} {'AVG SALARY':>13} {'TOTAL COST':>13}")
    print("  " + "-" * 50)
    for d in Department.with_stats():
        print(f"  {d[1]:<14} {d[3]:>6} {money(d[4]):>13} {money(d[5]):>13}")

    print("\n  " + "-" * 60)
    print("\n  TOP 5 EARNERS:\n")
    for i, r in enumerate(Employee.top_earners(5), 1):
        print(f"    {i}. {r[1]:<18} {money(r[4]):>10}   {r[5] or '-'}")
    print()


# ================================================================
# FEATURE 9 — EXPORT TO CSV  (Step 5 ka use)
# ================================================================

def export_csv():
    header("9. EXPORT TO CSV")

    out = Path(__file__).parent / "exports"
    out.mkdir(exist_ok=True)
    filename = out / f"employees_{datetime.now():%Y%m%d_%H%M%S}.csv"

    rows = Employee.all()
    headers = ["ID", "Name", "Email", "Phone", "Salary",
               "Department", "Designation", "Hire Date", "City", "Status"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"\n  ✅ {len(rows)} employees export ho gaye")
    print(f"  📁 File: {filename}")
    print("\n  (Step 5 me jo csv module seekha, wahi yahan use hua)\n")


# ================================================================
# MAIN MENU
# ================================================================

MENU = """
    ┌──────────────────────────────────────────────┐
    │   1. Add Employee                            │
    │   2. View Employees                          │
    │   3. Search Employee                         │
    │   4. Update Employee                         │
    │   5. Delete Employee                         │
    │   6. Search by Department                    │
    │   7. Salary Filtering                        │
    │   8. Statistics Dashboard                    │
    │   9. Export to CSV                           │
    │  10. Reset Database (sample data wapas)      │
    │   0. Exit                                    │
    └──────────────────────────────────────────────┘
"""


def main():
    init_db()

    print("\n" + "=" * 78)
    print(f"  {APP_NAME}  v{APP_VERSION}")
    print(f"  Database: {db_info()}")
    print("=" * 78)

    actions = {
        "1": add_employee,
        "2": view_employees,
        "3": search_employee,
        "4": update_employee,
        "5": delete_employee,
        "6": search_by_department,
        "7": salary_filtering,
        "8": statistics,
        "9": export_csv,
    }

    while True:
        print(MENU)
        try:
            choice = input("  Choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Bye! 👋\n")
            break

        if choice == "0":
            print("\n  Bye! 👋\n")
            break

        if choice == "10":
            confirm = input("  Sab data reset ho jaayega. Sure? (yes/no): ").strip()
            if confirm.lower() == "yes":
                reset_db()
                print("\n  ✅ Database reset ho gaya")
            pause()
            continue

        action = actions.get(choice)
        if action:
            try:
                action()
            except (EOFError, KeyboardInterrupt):
                print("\n  Cancelled")
            except Exception as e:
                print(f"\n  ❌ Unexpected error: {type(e).__name__}: {e}")
            pause()
        else:
            print("\n  ⚠️  Galat choice. 0-10 me se chuno.")


if __name__ == "__main__":
    main()
