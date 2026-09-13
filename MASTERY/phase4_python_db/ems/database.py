"""
================================================================
EMS — DATABASE LAYER
================================================================
Ye file connection handle karti hai.

YE FLOW YAAD RAKH (interview me poochhte hain):

    Python
      ↓
    MySQL / SQLite
      ↓
    CONNECTION      <- database se link
      ↓
    CURSOR          <- queries chalane ka tool
      ↓
    SQL QUERY       <- execute()
      ↓
    RESULT          <- fetchone() / fetchall()
      ↓
    CLOSE           <- cursor.close(), conn.close()
================================================================
"""

import sqlite3
from contextlib import contextmanager

from config import DB_TYPE, SQLITE_PATH, MYSQL_CONFIG, q


# ================================================================
# SCHEMA
# ================================================================

SQLITE_SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE,
    location        TEXT
);

CREATE TABLE IF NOT EXISTS employees (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    email         TEXT UNIQUE,
    phone         TEXT,
    salary        REAL CHECK (salary >= 0),
    department_id INTEGER,
    designation   TEXT,
    hire_date     TEXT,
    city          TEXT,
    status        TEXT DEFAULT 'Active',
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_emp_name   ON employees(name);
CREATE INDEX IF NOT EXISTS idx_emp_salary ON employees(salary);
CREATE INDEX IF NOT EXISTS idx_emp_dept   ON employees(department_id);
"""

MYSQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    location        VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS employees (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(120) UNIQUE,
    phone         VARCHAR(20),
    salary        DECIMAL(10,2) CHECK (salary >= 0),
    department_id INT,
    designation   VARCHAR(80),
    hire_date     DATE,
    city          VARCHAR(60),
    status        VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    INDEX idx_emp_name (name),
    INDEX idx_emp_salary (salary),
    INDEX idx_emp_dept (department_id)
) ENGINE=InnoDB;
"""

SEED_DEPARTMENTS = [
    ("IT", "Hyderabad"),
    ("HR", "Mumbai"),
    ("Sales", "Delhi"),
    ("Finance", "Mumbai"),
    ("Marketing", "Bangalore"),
]

SEED_EMPLOYEES = [
    ("Noman Syed",    "noman@techcorp.com",  "9876543210", 30000, 1, "Junior Developer",  "2026-01-10", "Hyderabad"),
    ("Sara Fatima",   "sara@techcorp.com",   "9876543211", 52000, 1, "Senior Developer",  "2022-08-05", "Hyderabad"),
    ("Ali Ahmed",     "ali@techcorp.com",    "9876543212", 45000, 2, "HR Executive",      "2023-04-12", "Mumbai"),
    ("Vikram Singh",  "vikram@techcorp.com", "9876543213", 67000, 3, "Sales Manager",     "2020-02-18", "Delhi"),
    ("Deepak Verma",  "deepak@techcorp.com", "9876543214", 95000, 4, "Finance Head",      "2019-05-14", "Mumbai"),
    ("Kavya Reddy",   "kavya@techcorp.com",  "9876543215", 64000, 5, "Marketing Lead",    "2021-07-19", "Bangalore"),
    ("Arjun Nair",    "arjun@techcorp.com",  "9876543216", 72000, 1, "Tech Lead",         "2021-03-08", "Bangalore"),
    ("Anjali Rao",    "anjali@techcorp.com", "9876543217", 48000, 3, "Sales Executive",   "2023-11-30", "Delhi"),
]


# ================================================================
# CONNECTION
# ================================================================

def get_connection():
    """
    Database se CONNECTION banao.

    Ye function hi DB_TYPE dekh ke decide karta hai ki
    SQLite khulegi ya MySQL. Baaki poora app ko fark nahi padta.
    """
    if DB_TYPE == "sqlite":
        conn = sqlite3.connect(SQLITE_PATH)
        conn.execute("PRAGMA foreign_keys = ON")    # SQLite me FK default OFF hota hai!
        conn.row_factory = sqlite3.Row              # dict jaisa access: row["name"]
        return conn

    elif DB_TYPE == "mysql":
        try:
            import mysql.connector
        except ImportError:
            raise ImportError(
                "mysql-connector-python installed nahi hai.\n"
                "Chalao:  pip install mysql-connector-python"
            )
        return mysql.connector.connect(**MYSQL_CONFIG)

    raise ValueError(f"Galat DB_TYPE: {DB_TYPE}. 'sqlite' ya 'mysql' hona chahiye.")


@contextmanager
def get_cursor(commit=False):
    """
    CONTEXT MANAGER — connection + cursor automatically khulta/band hota hai.

    Use:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM employees")
            rows = cur.fetchall()

    Faida:
      - close() khud bhoolne ka chance nahi
      - error aaye to ROLLBACK automatic
      - success pe COMMIT automatic (agar commit=True)

    Ye 'with open(file)' jaisa hi pattern hai.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()      # ⚠️ error pe sab cancel — transaction safety
        raise
    finally:
        cursor.close()
        conn.close()


# ================================================================
# QUERY HELPERS
# ================================================================

def fetch_all(sql, params=()):
    """SELECT chalao, saari rows lao (list of tuples)."""
    with get_cursor() as cur:
        cur.execute(q(sql), params)
        return cur.fetchall()


def fetch_one(sql, params=()):
    """SELECT chalao, sirf pehli row lao."""
    with get_cursor() as cur:
        cur.execute(q(sql), params)
        return cur.fetchone()


def execute(sql, params=()):
    """INSERT / UPDATE / DELETE chalao. Affected rows return karta hai."""
    with get_cursor(commit=True) as cur:
        cur.execute(q(sql), params)
        return cur.rowcount


def execute_returning_id(sql, params=()):
    """INSERT chalao aur nayi row ka ID wapas lao."""
    with get_cursor(commit=True) as cur:
        cur.execute(q(sql), params)
        return cur.lastrowid


def execute_many(sql, param_list):
    """Bulk INSERT — ek ek karke insert karne se bahut FAST."""
    with get_cursor(commit=True) as cur:
        cur.executemany(q(sql), param_list)
        return cur.rowcount


# ================================================================
# SETUP
# ================================================================

def init_db(seed=True):
    """Tables banao aur sample data daalo."""
    conn = get_connection()
    cursor = conn.cursor()

    schema = SQLITE_SCHEMA if DB_TYPE == "sqlite" else MYSQL_SCHEMA
    for statement in schema.split(";"):
        if statement.strip():
            cursor.execute(statement)
    conn.commit()

    if seed:
        cursor.execute("SELECT COUNT(*) FROM departments")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                q("INSERT INTO departments (department_name, location) VALUES (?, ?)"),
                SEED_DEPARTMENTS,
            )
            conn.commit()

        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                q("""INSERT INTO employees
                     (name, email, phone, salary, department_id,
                      designation, hire_date, city)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""),
                SEED_EMPLOYEES,
            )
            conn.commit()

    cursor.close()
    conn.close()


def reset_db():
    """Sab mita ke dobara banao (testing ke liye)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS employees")
    cursor.execute("DROP TABLE IF EXISTS departments")
    conn.commit()
    cursor.close()
    conn.close()
    init_db(seed=True)


def db_info():
    """Connection ki detail (UI me dikhane ke liye)."""
    if DB_TYPE == "sqlite":
        return f"SQLite  ({SQLITE_PATH.name})"
    return f"MySQL   ({MYSQL_CONFIG['user']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']})"


# ================================================================
# RAW DEMO — bina helper ke, poora flow dikhane ke liye
# ================================================================

def raw_flow_demo():
    """
    Interview me jab poochhein "Python se database kaise connect karte ho?"
    to ye 6 step bolna.
    """
    print("\n  RAW FLOW (helpers ke bina):\n")

    # STEP 1: CONNECTION
    conn = get_connection()
    print("    1. CONNECTION  -> conn = sqlite3.connect('ems.db')")

    # STEP 2: CURSOR
    cursor = conn.cursor()
    print("    2. CURSOR      -> cursor = conn.cursor()")

    # STEP 3: EXECUTE (parameterized — SQL injection safe)
    cursor.execute(q("SELECT id, name, salary FROM employees WHERE salary > ?"), (40000,))
    print("    3. EXECUTE     -> cursor.execute(sql, params)")

    # STEP 4: FETCH
    rows = cursor.fetchall()
    print(f"    4. FETCH       -> cursor.fetchall()   ({len(rows)} rows mili)")
    for r in rows[:3]:
        print(f"                      {r[0]}. {r[1]} - {r[2]}")

    # STEP 5: COMMIT (sirf write operations pe)
    print("    5. COMMIT      -> conn.commit()   (INSERT/UPDATE/DELETE ke baad)")

    # STEP 6: CLOSE
    cursor.close()
    conn.close()
    print("    6. CLOSE       -> cursor.close(); conn.close()")

    print("\n    fetchone()  -> ek row")
    print("    fetchall()  -> saari rows")
    print("    fetchmany(n)-> n rows")


if __name__ == "__main__":
    print("=" * 62)
    print("DATABASE LAYER TEST")
    print("=" * 62)
    print(f"\n  DB: {db_info()}")
    init_db()
    print("  ✅ Tables ready")

    count = fetch_one("SELECT COUNT(*) FROM employees")[0]
    print(f"  ✅ {count} employees in database")

    raw_flow_demo()
