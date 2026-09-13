-- ================================================================
-- STEP 11 — AGGREGATE FUNCTIONS  🔴🔴
-- COUNT, SUM, AVG, MIN, MAX + GROUP BY, HAVING, ORDER BY
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step11_aggregates.sql
--
-- Aggregate = bahut saari rows ko ek value me badalna.
-- Data Analyst ka 70% kaam yahi hai.
-- ================================================================


-- ================================================================
-- 1. PAANCH AGGREGATE FUNCTIONS
-- ================================================================

SELECT
    COUNT(*)      AS total_rows,
    COUNT(salary) AS salary_wale,      -- NULL count nahi hote!
    SUM(salary)   AS total_salary,
    AVG(salary)   AS average_salary,
    MIN(salary)   AS lowest,
    MAX(salary)   AS highest
FROM employees;

-- ⚠️ COUNT(*) vs COUNT(column) — YE INTERVIEW ME POOCHHTE HAIN
--    COUNT(*)       -> saari rows ginta hai (NULL bhi)
--    COUNT(column)  -> sirf NON-NULL values ginta hai
--    Upar dekho: total_rows = 20, salary_wale = 18 (2 NULL hain)

-- COUNT(DISTINCT ...) — unique count
SELECT
    COUNT(*)                AS total_employees,
    COUNT(DISTINCT city)    AS unique_cities,
    COUNT(DISTINCT department_id) AS unique_depts
FROM employees;

-- ROUND se decimal control
SELECT
    ROUND(AVG(salary), 2) AS avg_salary,
    ROUND(AVG(salary))    AS avg_rounded
FROM employees;


-- ================================================================
-- 2. GROUP BY — category wise summary
-- ================================================================
-- Tera example:
--   SELECT department, AVG(salary) FROM employees GROUP BY department;

-- City ke hisaab se
SELECT
    city,
    COUNT(*)              AS employees,
    ROUND(AVG(salary), 0) AS avg_salary,
    MAX(salary)           AS highest,
    MIN(salary)           AS lowest
FROM employees
WHERE salary IS NOT NULL
GROUP BY city
ORDER BY avg_salary DESC;

-- Department ke hisaab se (JOIN ke saath — naam dikhega)
SELECT
    d.department_name,
    COUNT(e.id)             AS employees,
    ROUND(AVG(e.salary), 0) AS avg_salary,
    SUM(e.salary)           AS total_cost
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.department_name
ORDER BY avg_salary DESC;

-- Multiple columns pe GROUP BY
SELECT
    city,
    department_id,
    COUNT(*)              AS count,
    ROUND(AVG(salary), 0) AS avg_salary
FROM employees
WHERE salary IS NOT NULL AND department_id IS NOT NULL
GROUP BY city, department_id
ORDER BY city, avg_salary DESC;

-- ⚠️ GOLDEN RULE:
--    SELECT me jo column hai wo ya GROUP BY me hona chahiye
--    ya aggregate function ke andar. Warna error/galat result.


-- ================================================================
-- 3. HAVING — groups ko filter karo
-- ================================================================
-- WHERE  -> ROWS filter karta hai  (GROUP BY se PEHLE)
-- HAVING -> GROUPS filter karta hai (GROUP BY ke BAAD)
-- Ye fark interview me 100% poochha jaata hai.

-- Sirf wo cities jahan 3 se zyada employees hain
SELECT city, COUNT(*) AS employees
FROM employees
GROUP BY city
HAVING COUNT(*) > 3
ORDER BY employees DESC;

-- Sirf wo departments jinki avg salary 55000 se zyada hai
SELECT
    d.department_name,
    COUNT(e.id)             AS employees,
    ROUND(AVG(e.salary), 0) AS avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.department_name
HAVING AVG(e.salary) > 55000
ORDER BY avg_salary DESC;

-- WHERE + HAVING dono ek saath
SELECT
    city,
    COUNT(*)              AS employees,
    ROUND(AVG(salary), 0) AS avg_salary
FROM employees
WHERE salary IS NOT NULL          -- pehle rows filter (WHERE)
GROUP BY city                      -- phir group
HAVING COUNT(*) >= 2               -- phir groups filter (HAVING)
ORDER BY avg_salary DESC;


-- ================================================================
-- 4. QUERY EXECUTION ORDER (BAHUT IMPORTANT)
-- ================================================================
-- Tum LIKHTE ho aise:
--   SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY -> LIMIT
--
-- SQL CHALATA hai aise:
--   1. FROM      (table lo)
--   2. WHERE     (rows filter)
--   3. GROUP BY  (groups banao)
--   4. HAVING    (groups filter)
--   5. SELECT    (columns chuno)
--   6. ORDER BY  (sort karo)
--   7. LIMIT     (kitni rows)
--
-- ISILIYE:
--   - WHERE me column alias use nahi kar sakte (SELECT baad me chalta hai)
--   - ORDER BY me alias use KAR SAKTE ho (SELECT pehle chal chuka)

-- Ye chalega (ORDER BY me alias):
SELECT name, salary * 12 AS annual FROM employees
WHERE salary IS NOT NULL
ORDER BY annual DESC LIMIT 3;

-- Ye MySQL me ERROR dega (WHERE me alias):
--   SELECT name, salary * 12 AS annual FROM employees WHERE annual > 500000;


-- ================================================================
-- 5. REAL WORLD REPORTS
-- ================================================================

-- Report 1: Department summary
SELECT
    d.department_name              AS department,
    d.location,
    COUNT(e.id)                    AS headcount,
    COALESCE(SUM(e.salary), 0)     AS monthly_cost,
    COALESCE(ROUND(AVG(e.salary)), 0) AS avg_salary,
    d.budget,
    ROUND(COALESCE(SUM(e.salary), 0) * 12.0 / d.budget * 100, 1) AS budget_used_pct
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.department_name, d.location, d.budget
ORDER BY monthly_cost DESC;

-- Report 2: Top customer by spending
SELECT
    c.name              AS customer,
    c.city,
    COUNT(o.id)         AS total_orders,
    SUM(o.amount)       AS total_spent,
    ROUND(AVG(o.amount)) AS avg_order_value,
    MAX(o.amount)       AS biggest_order
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.city
ORDER BY total_spent DESC;

-- Report 3: Product category analysis
SELECT
    category,
    COUNT(*)          AS products,
    SUM(stock)        AS total_stock,
    ROUND(AVG(price)) AS avg_price,
    MIN(price)        AS cheapest,
    MAX(price)        AS costliest
FROM products
GROUP BY category
ORDER BY avg_price DESC;

-- Report 4: Monthly sales trend
SELECT
    SUBSTR(order_date, 1, 7) AS month,
    COUNT(*)                 AS orders,
    SUM(amount)              AS revenue,
    ROUND(AVG(amount))       AS avg_order
FROM orders
GROUP BY SUBSTR(order_date, 1, 7)
ORDER BY month;

-- Report 5: Project hours by employee
SELECT
    e.name,
    COUNT(a.project_id) AS projects,
    SUM(a.hours)        AS total_hours,
    ROUND(AVG(a.hours)) AS avg_hours
FROM employees e
JOIN assignments a ON e.id = a.employee_id
GROUP BY e.id, e.name
HAVING COUNT(a.project_id) > 1
ORDER BY total_hours DESC;


-- ================================================================
-- 6. AGGREGATE + CONDITIONAL (conditional aggregation)
-- ================================================================
-- Ye advanced trick hai — interview me impress karta hai

SELECT
    city,
    COUNT(*)                                          AS total,
    SUM(CASE WHEN salary > 50000 THEN 1 ELSE 0 END)   AS high_earners,
    SUM(CASE WHEN salary <= 50000 THEN 1 ELSE 0 END)  AS others,
    ROUND(AVG(CASE WHEN salary > 50000 THEN salary END)) AS avg_high_salary
FROM employees
WHERE salary IS NOT NULL
GROUP BY city
ORDER BY high_earners DESC;


-- ================================================================
-- INTERVIEW QUESTIONS
-- ================================================================
-- Q1. COUNT(*) vs COUNT(column) vs COUNT(1)?
--     COUNT(*)      -> saari rows (NULL bhi)
--     COUNT(column) -> sirf non-NULL values
--     COUNT(1)      -> COUNT(*) jaisa hi, performance same
--
-- Q2. WHERE vs HAVING?
--     WHERE  -> individual ROWS pe, GROUP BY se pehle, aggregate nahi chalta
--     HAVING -> GROUPS pe, GROUP BY ke baad, aggregate chalta hai
--
-- Q3. GROUP BY me SELECT ka rule?
--     SELECT me har column ya GROUP BY me ho ya aggregate ke andar ho.
--
-- Q4. Query execution order?
--     FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
--
-- Q5. AVG NULL ko kaise treat karta hai?
--     Ignore karta hai. AVG(salary) = SUM(salary) / COUNT(salary),
--     NOT / COUNT(*). Isliye NULL wali rows count nahi hoti.
--
-- Q6. Aggregate function WHERE me kyun nahi chalta?
--     WHERE, GROUP BY se PEHLE chalta hai — tab tak groups bane hi nahi.
--     Isliye HAVING use karo.


-- ================================================================
-- PRACTICE
-- ================================================================
-- 1.  Total employees kitne hain?
-- 2.  Average salary kya hai?
-- 3.  Sabse zyada aur sabse kam salary?
-- 4.  Har city me kitne employees?
-- 5.  Har department ki average salary
-- 6.  Wo cities jahan 2 se zyada employees hain
-- 7.  Wo departments jinki total salary 200000 se zyada hai
-- 8.  Har customer ne kitne orders kiye?
-- 9.  Har product category ka total stock
-- 10. Mahine ke hisaab se total revenue
-- 11. Jin employees ne 2 se zyada project kiye
-- 12. Har city me 50000+ salary wale kitne hain (conditional aggregation)
