-- ================================================================
-- STEP 9 — SQL BASICS  🔴🔴🔴  (CREATE, INSERT, SELECT, UPDATE, DELETE)
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step09_basics.sql
--
-- CRUD = Create, Read, Update, Delete
-- Ye 5 commands SQL ka 80% kaam karte hain.
-- ================================================================


-- ================================================================
-- PART 1: CREATE TABLE
-- ================================================================
-- Ye tera diya hua example hai:
--
--   CREATE TABLE employees (
--       id INT PRIMARY KEY,
--       name VARCHAR(100),
--       salary INT
--   );
--
-- MySQL me: INT, VARCHAR(100)
-- SQLite me: INTEGER, TEXT
-- (concept bilkul same hai)

DROP TABLE IF EXISTS demo_employees;

CREATE TABLE demo_employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    salary     INTEGER,
    department TEXT DEFAULT 'General',
    email      TEXT UNIQUE
);

-- CONSTRAINTS samjho:
--   PRIMARY KEY -> unique + not null, har row ki pehchaan
--   NOT NULL    -> khaali nahi chhod sakte
--   UNIQUE      -> duplicate nahi
--   DEFAULT     -> na do to ye value lagegi
--   CHECK       -> condition
--   FOREIGN KEY -> dusri table se link


-- ================================================================
-- PART 2: INSERT
-- ================================================================
-- Tera example:
--   INSERT INTO employees VALUES (1, 'Noman', 30000);

-- Tareeka 1: column names ke saath (BEST — hamesha aise likho)
INSERT INTO demo_employees (id, name, salary, department, email)
VALUES (1, 'Noman', 30000, 'IT', 'noman@demo.com');

-- Tareeka 2: bina column names (order exact hona chahiye — risky)
INSERT INTO demo_employees
VALUES (2, 'Ali', 45000, 'HR', 'ali@demo.com');

-- Tareeka 3: MULTIPLE rows ek saath (FAST — ye use karo)
INSERT INTO demo_employees (id, name, salary, department, email) VALUES
 (3, 'Sara',  52000, 'IT',      'sara@demo.com'),
 (4, 'Zoya',  38000, 'Sales',   'zoya@demo.com'),
 (5, 'Imran', 41000, 'HR',      'imran@demo.com');

-- Tareeka 4: kuch columns chhod do -> DEFAULT ya NULL lagega
INSERT INTO demo_employees (id, name, salary)
VALUES (6, 'Rahul', 35000);
-- department = 'General' (default), email = NULL


-- ================================================================
-- PART 3: SELECT — data padhna
-- ================================================================

-- Sab kuch
SELECT * FROM demo_employees;

-- Sirf specific columns (production me * kabhi mat likho)
SELECT name, salary FROM demo_employees;

-- ALIAS (AS) — column ka naam badlo output me
SELECT name AS employee_name, salary AS monthly_salary
FROM demo_employees;

-- CALCULATED column
SELECT name, salary, salary * 12 AS annual_salary
FROM demo_employees;

-- DISTINCT — unique values
SELECT DISTINCT department FROM demo_employees;

-- LIMIT — kitni rows chahiye
SELECT * FROM demo_employees LIMIT 3;

-- ORDER BY + LIMIT — top N nikalne ka tareeka
SELECT name, salary FROM demo_employees
ORDER BY salary DESC
LIMIT 3;


-- ================================================================
-- PART 4: UPDATE
-- ================================================================
-- Tera example:
--   UPDATE employees SET salary = 35000 WHERE id = 1;
--
-- ⚠️  WHERE BHOOL GAYE = POORI TABLE UPDATE HO JAAYEGI ⚠️
-- Ye sabse badi SQL galti hai. Hamesha WHERE likho.

UPDATE demo_employees
SET salary = 35000
WHERE id = 1;

SELECT id, name, salary FROM demo_employees WHERE id = 1;

-- Multiple columns ek saath
UPDATE demo_employees
SET salary = 48000, department = 'IT'
WHERE id = 5;

-- Calculation ke saath — sabko 10% raise
UPDATE demo_employees
SET salary = salary * 1.10
WHERE department = 'IT';

SELECT name, salary, department FROM demo_employees WHERE department = 'IT';

-- SAFE UPDATE TIP:
-- Pehle SELECT chalao same WHERE ke saath, dekho kitni rows aati hain.
-- Sahi lage to UPDATE chalao.


-- ================================================================
-- PART 5: DELETE
-- ================================================================
-- Tera example:
--   DELETE FROM employees WHERE id = 1;
--
-- ⚠️  DELETE FROM table;  <- WHERE bina = SAB DELETE

DELETE FROM demo_employees
WHERE id = 6;

SELECT COUNT(*) AS bache_hue FROM demo_employees;

-- Condition ke saath delete
DELETE FROM demo_employees
WHERE salary < 40000;

SELECT * FROM demo_employees;


-- ================================================================
-- PART 6: ASLI TABLES PE PRACTICE
-- ================================================================

-- Saare employees
SELECT id, name, salary, department_id FROM employees LIMIT 8;

-- Naam aur salary, salary ke hisaab se sorted
SELECT name, salary FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC
LIMIT 5;

-- Departments
SELECT * FROM departments;

-- Alag alag cities
SELECT DISTINCT city FROM employees ORDER BY city;

-- Annual salary calculate
SELECT name, salary, salary * 12 AS annual, salary * 0.10 AS tax
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC
LIMIT 5;


-- ================================================================
-- PART 7: DDL vs DML vs DCL vs TCL  (INTERVIEW ME POOCHHTE HAIN)
-- ================================================================
-- DDL (Data Definition Language)   -> CREATE, ALTER, DROP, TRUNCATE
-- DML (Data Manipulation Language) -> INSERT, UPDATE, DELETE, SELECT
-- DCL (Data Control Language)      -> GRANT, REVOKE
-- TCL (Transaction Control)        -> COMMIT, ROLLBACK, SAVEPOINT
--
-- DELETE vs TRUNCATE vs DROP:
--   DELETE   -> rows hatata hai, WHERE laga sakte ho, rollback ho sakta hai (DML)
--   TRUNCATE -> saari rows, WHERE nahi, fast, rollback nahi (DDL)
--   DROP     -> poori TABLE hi gayab (DDL)


-- ================================================================
-- PRACTICE — khud likho (solutions: solutions/step09_solutions.sql)
-- ================================================================
-- 1.  'students' table banao: id, name, marks, grade
-- 2.  Usme 5 students insert karo
-- 3.  Saare students dikhao
-- 4.  Sirf name aur marks dikhao
-- 5.  Marks ke hisaab se descending sort karo
-- 6.  Top 3 students nikalo
-- 7.  Ek student ke marks update karo
-- 8.  Sab students ke marks me 5 add karo
-- 9.  40 se kam marks wale delete karo
-- 10. employees table se top 5 salary wale nikalo
-- 11. DISTINCT city list nikalo employees se
-- 12. Har employee ki annual salary (salary * 12) dikhao
