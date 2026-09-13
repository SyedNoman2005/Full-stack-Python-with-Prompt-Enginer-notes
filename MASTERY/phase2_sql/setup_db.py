"""
================================================================
SQL PRACTICE DATABASE — SETUP
================================================================
Chalane ke liye:  python3 phase2_sql/setup_db.py

Ye SQLite database banata hai practice ke liye — zero setup.
Syntax 95% MySQL jaisa hai.

TABLES:
  departments  (5 rows)
  employees    (20 rows)  -- kuch NULL values jaan bujh ke
  projects     (8 rows)
  assignments  (15 rows)  -- many-to-many
  customers    (8 rows)   -- kuch ne order nahi kiya (LEFT JOIN practice)
  orders       (12 rows)
  products     (10 rows)
================================================================
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "practice.db"


SCHEMA = """
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

CREATE TABLE departments (
    id              INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE,
    location        TEXT,
    budget          INTEGER
);

CREATE TABLE employees (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    email         TEXT UNIQUE,
    salary        INTEGER,
    department_id INTEGER,
    manager_id    INTEGER,
    hire_date     TEXT,
    city          TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (manager_id)    REFERENCES employees(id)
);

CREATE TABLE projects (
    id           INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    budget       INTEGER,
    start_date   TEXT,
    end_date     TEXT,
    status       TEXT
);

CREATE TABLE assignments (
    id          INTEGER PRIMARY KEY,
    employee_id INTEGER,
    project_id  INTEGER,
    hours       INTEGER,
    role        TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (project_id)  REFERENCES projects(id)
);

CREATE TABLE customers (
    id       INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    email    TEXT,
    city     TEXT,
    country  TEXT DEFAULT 'India'
);

CREATE TABLE products (
    id       INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    category TEXT,
    price    INTEGER,
    stock    INTEGER
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id  INTEGER,
    quantity    INTEGER,
    order_date  TEXT,
    amount      INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id)  REFERENCES products(id)
);
"""


DATA = """
INSERT INTO departments (id, department_name, location, budget) VALUES
 (1, 'IT',        'Hyderabad', 5000000),
 (2, 'HR',        'Mumbai',    1500000),
 (3, 'Sales',     'Delhi',     3000000),
 (4, 'Finance',   'Mumbai',    2500000),
 (5, 'Marketing', 'Bangalore', 2000000);

-- Note: id 4 (Zoya) ka department NULL hai, id 20 ka bhi
-- Note: kuch logon ki salary NULL hai (intern)
INSERT INTO employees (id, name, email, salary, department_id, manager_id, hire_date, city) VALUES
 (1,  'Rajesh Kumar',  'rajesh@techcorp.com',  120000, 1,    NULL, '2018-01-15', 'Hyderabad'),
 (2,  'Priya Sharma',  'priya@techcorp.com',   110000, 2,    NULL, '2018-03-20', 'Mumbai'),
 (3,  'Noman Syed',    'noman@techcorp.com',    30000, 1,    1,    '2026-01-10', 'Hyderabad'),
 (4,  'Zoya Khan',     'zoya@techcorp.com',     38000, NULL, NULL, '2025-06-01', 'Delhi'),
 (5,  'Ali Ahmed',     'ali@techcorp.com',      45000, 2,    2,    '2023-04-12', 'Mumbai'),
 (6,  'Sara Fatima',   'sara@techcorp.com',     52000, 1,    1,    '2022-08-05', 'Hyderabad'),
 (7,  'Vikram Singh',  'vikram@techcorp.com',   67000, 3,    NULL, '2020-02-18', 'Delhi'),
 (8,  'Anjali Rao',    'anjali@techcorp.com',   48000, 3,    7,    '2023-11-30', 'Delhi'),
 (9,  'Imran Ali',     'imran@techcorp.com',    41000, 3,    7,    '2024-01-22', 'Mumbai'),
 (10, 'Deepak Verma',  'deepak@techcorp.com',   95000, 4,    NULL, '2019-05-14', 'Mumbai'),
 (11, 'Sneha Patel',   'sneha@techcorp.com',    58000, 4,    10,   '2022-09-01', 'Mumbai'),
 (12, 'Arjun Nair',    'arjun@techcorp.com',    72000, 1,    1,    '2021-03-08', 'Bangalore'),
 (13, 'Kavya Reddy',   'kavya@techcorp.com',    64000, 5,    NULL, '2021-07-19', 'Bangalore'),
 (14, 'Rohit Mehta',   'rohit@techcorp.com',    39000, 5,    13,   '2024-05-25', 'Bangalore'),
 (15, 'Fatima Sheikh', 'fatima@techcorp.com',   55000, 1,    1,    '2022-12-11', 'Hyderabad'),
 (16, 'Suresh Babu',   'suresh@techcorp.com',   43000, 3,    7,    '2023-06-17', 'Hyderabad'),
 (17, 'Meera Joshi',   'meera@techcorp.com',    88000, 4,    10,   '2020-10-03', 'Delhi'),
 (18, 'Karan Malhotra','karan@techcorp.com',    35000, 5,    13,   '2025-02-14', 'Delhi'),
 (19, 'Aisha Begum',   'aisha@techcorp.com',      NULL, 1,   1,    '2026-02-01', 'Hyderabad'),
 (20, 'Rahul Gupta',   'rahul@techcorp.com',      NULL, NULL, NULL, '2026-03-01', 'Pune');

INSERT INTO projects (id, project_name, budget, start_date, end_date, status) VALUES
 (1, 'E-Commerce Platform', 1500000, '2025-01-01', '2026-06-30', 'Active'),
 (2, 'Mobile Banking App',  2000000, '2025-03-15', '2026-09-30', 'Active'),
 (3, 'HR Portal',            500000, '2024-06-01', '2025-03-31', 'Completed'),
 (4, 'Data Warehouse',      1800000, '2025-08-01', '2026-12-31', 'Active'),
 (5, 'CRM System',           900000, '2024-01-10', '2024-12-20', 'Completed'),
 (6, 'AI Chatbot',           750000, '2026-01-05', '2026-08-31', 'Active'),
 (7, 'Legacy Migration',     600000, '2025-05-01', NULL,         'On Hold'),
 (8, 'Analytics Dashboard',  450000, '2026-02-01', NULL,         'Planning');

INSERT INTO assignments (id, employee_id, project_id, hours, role) VALUES
 (1,  3,  1, 160, 'Developer'),
 (2,  6,  1, 180, 'Senior Developer'),
 (3,  12, 1, 200, 'Tech Lead'),
 (4,  15, 2, 170, 'Developer'),
 (5,  1,  2, 120, 'Architect'),
 (6,  6,  2, 140, 'Senior Developer'),
 (7,  5,  3, 100, 'HR Analyst'),
 (8,  2,  3,  80, 'Project Manager'),
 (9,  12, 4, 190, 'Tech Lead'),
 (10, 3,  4, 150, 'Developer'),
 (11, 17, 4, 110, 'Data Analyst'),
 (12, 13, 5, 130, 'Marketing Lead'),
 (13, 14, 5,  90, 'Associate'),
 (14, 15, 6, 160, 'Developer'),
 (15, 1,  6, 100, 'Architect');

INSERT INTO customers (id, name, email, city, country) VALUES
 (1, 'Amit Traders',    'amit@trade.com',    'Hyderabad', 'India'),
 (2, 'Beta Retail',     'info@beta.com',     'Mumbai',    'India'),
 (3, 'Global Supplies', 'sales@global.com',  'Delhi',     'India'),
 (4, 'Kiran Stores',    'kiran@stores.com',  'Chennai',   'India'),
 (5, 'Modern Mart',     NULL,                'Bangalore', 'India'),
 (6, 'Nova Enterprise', 'nova@ent.com',      'Pune',      'India'),
 (7, 'Star Wholesale',  'star@whole.com',    'Kolkata',   'India'),
 (8, 'Zenith Corp',     'zenith@corp.com',   'Dubai',     'UAE');

INSERT INTO products (id, name, category, price, stock) VALUES
 (1,  'Laptop',        'Electronics', 55000, 25),
 (2,  'Mouse',         'Electronics',   700, 200),
 (3,  'Keyboard',      'Electronics',  1500, 150),
 (4,  'Monitor',       'Electronics', 12000, 40),
 (5,  'Office Chair',  'Furniture',    8500, 30),
 (6,  'Desk',          'Furniture',   15000, 20),
 (7,  'Notebook',      'Stationery',     60, 500),
 (8,  'Pen Set',       'Stationery',    250, 300),
 (9,  'Headphones',    'Electronics',  3200, 80),
 (10, 'Webcam',        'Electronics',  2800, 0);

-- Customers 4, 5, 8 ne KABHI order nahi kiya (LEFT JOIN practice ke liye)
INSERT INTO orders (id, customer_id, product_id, quantity, order_date, amount) VALUES
 (1,  1, 1,  2, '2026-01-05', 110000),
 (2,  1, 2,  5, '2026-01-05',   3500),
 (3,  2, 4,  3, '2026-01-12',  36000),
 (4,  3, 1,  1, '2026-01-20',  55000),
 (5,  2, 5,  4, '2026-02-02',  34000),
 (6,  6, 9,  2, '2026-02-14',   6400),
 (7,  1, 6,  1, '2026-02-18',  15000),
 (8,  7, 3, 10, '2026-03-01',  15000),
 (9,  3, 7, 50, '2026-03-07',   3000),
 (10, 2, 1,  1, '2026-03-15',  55000),
 (11, 6, 8, 20, '2026-04-02',   5000),
 (12, 7, 4,  2, '2026-04-10',  24000);
"""


def setup():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.executescript(DATA)
    conn.commit()

    print("=" * 62)
    print("SQL PRACTICE DATABASE BAN GAYA")
    print("=" * 62)
    print(f"File: {DB_PATH}\n")

    cur = conn.cursor()
    tables = ["departments", "employees", "projects", "assignments",
              "customers", "products", "orders"]

    print(f"  {'TABLE':<15} {'ROWS':>6}   COLUMNS")
    print("  " + "-" * 70)
    for t in tables:
        count = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        cols = [r[1] for r in cur.execute(f"PRAGMA table_info({t})")]
        print(f"  {t:<15} {count:>6}   {', '.join(cols)}")

    print("\n  JAAN BUJH KE DAALA GAYA (practice ke liye):")
    print("    - employees.department_id me NULL (id 4, 20)")
    print("    - employees.salary me NULL (id 19, 20)")
    print("    - employees.manager_id se SELF JOIN practice")
    print("    - customers 4, 5, 8 ne koi order nahi kiya -> LEFT JOIN")
    print("    - products.stock = 0 (Webcam) -> filtering")
    print("    - projects.end_date me NULL -> IS NULL")

    conn.close()

    print("\n" + "=" * 62)
    print("AB YE CHALAO:")
    print("  python3 phase2_sql/run_sql.py phase2_sql/step09_basics.sql")
    print("  python3 phase2_sql/run_sql.py phase2_sql/step12_joins.sql")
    print("\nYa interactive mode:")
    print("  python3 phase2_sql/run_sql.py")
    print("=" * 62)


if __name__ == "__main__":
    setup()
