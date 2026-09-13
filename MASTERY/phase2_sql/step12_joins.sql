-- ================================================================
-- STEP 12 — JOINS  🔥🔥🔥  (SABSE IMPORTANT SQL TOPIC)
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step12_joins.sql
--
-- JOIN = do ya zyada tables ko jodna common column se.
-- Har SQL interview me JOIN 100% aata hai.
--
-- MINIMUM: INNER + LEFT + RIGHT achhe se aane chahiye.
-- ================================================================


-- ================================================================
-- 0. PEHLE DATA SAMJHO
-- ================================================================

SELECT id, department_name FROM departments;

-- Dhyan do: id 4 (Zoya) aur id 20 (Rahul) ka department_id NULL hai
SELECT id, name, department_id FROM employees ORDER BY id;


-- ================================================================
-- 1. INNER JOIN — sirf MATCHING rows
-- ================================================================
-- Tera example:
--   SELECT e.name, d.department_name
--   FROM employees e
--   JOIN departments d ON e.department_id = d.id;
--
-- Venn diagram: do circles ka BEECH ka hissa (intersection)
-- Jinka match nahi mila, wo DROP ho jaate hain.

SELECT
    e.name          AS employee,
    d.department_name AS department,
    d.location
FROM employees e
INNER JOIN departments d ON e.department_id = d.id
ORDER BY d.department_name, e.name;

-- ^^ Dhyan do: Zoya aur Rahul NAHI dikhe (unka department NULL hai)
--    INNER JOIN unhe drop kar deta hai. Ye important behaviour hai.

-- Count compare karo
SELECT COUNT(*) AS total_employees FROM employees;
SELECT COUNT(*) AS inner_join_result
FROM employees e INNER JOIN departments d ON e.department_id = d.id;
-- 20 vs 18 — 2 rows kho gayi!

-- JOIN = INNER JOIN (INNER optional hai)
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
LIMIT 5;

-- 3 TABLES ka JOIN
SELECT
    e.name        AS employee,
    d.department_name AS department,
    p.project_name,
    a.hours,
    a.role
FROM employees e
JOIN departments d  ON e.department_id = d.id
JOIN assignments a  ON e.id = a.employee_id
JOIN projects p     ON a.project_id = p.id
ORDER BY p.project_name, e.name;


-- ================================================================
-- 2. LEFT JOIN — LEFT table ki SAARI rows + matching right
-- ================================================================
-- LEFT table sab aayenge. Right me match nahi mila to NULL.
-- Ye sabse zyada use hone wala JOIN hai real projects me.

SELECT
    e.id,
    e.name              AS employee,
    d.department_name   AS department
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id
ORDER BY e.id;

-- ^^ Ab Zoya aur Rahul BHI dikhenge, department NULL ke saath.

-- LEFT JOIN ka SABSE BADA USE: "kis ka kuch nahi hai?" dhoondhna
-- Jinhone KABHI order nahi kiya:
SELECT
    c.id,
    c.name  AS customer,
    c.city
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
-- ^^ customers 4, 5, 8 — inhone kabhi order nahi kiya
--    Ye pattern "anti-join" kehlata hai. INTERVIEW FAVOURITE.

-- Employees jinhe koi project nahi mila:
SELECT e.name
FROM employees e
LEFT JOIN assignments a ON e.id = a.employee_id
WHERE a.id IS NULL
ORDER BY e.name;

-- Departments jinme koi employee nahi:
SELECT d.department_name
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
WHERE e.id IS NULL;

-- Products jo kabhi bike hi nahi:
SELECT p.name, p.category, p.price
FROM products p
LEFT JOIN orders o ON p.id = o.product_id
WHERE o.id IS NULL;

-- LEFT JOIN with aggregate — customer with order count (0 bhi dikhega)
SELECT
    c.name                  AS customer,
    COUNT(o.id)             AS orders,
    COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_spent DESC;

-- ⚠️ BADA TRAP: LEFT JOIN me condition WHERE me daali to wo INNER JOIN ban jaata hai!
-- GALAT (INNER JOIN jaisa behave karega):
SELECT c.name, o.amount
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.amount > 10000;

-- SAHI (condition ON me daalo):
SELECT c.name, o.amount
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id AND o.amount > 10000
ORDER BY c.name;


-- ================================================================
-- 3. RIGHT JOIN — RIGHT table ki saari rows
-- ================================================================
-- LEFT JOIN ka ulta. Tables swap kar do to LEFT JOIN ban jaata hai.
-- Practice me log RIGHT JOIN kam use karte hain.
--
-- NOTE: SQLite 3.39+ me RIGHT JOIN support hai.
--       Purane SQLite me nahi chalta. MySQL me poora support hai.

SELECT
    d.department_name,
    e.name AS employee
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id
ORDER BY d.department_name;

-- Ye same result LEFT JOIN se (tables swap karke):
SELECT
    d.department_name,
    e.name AS employee
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
ORDER BY d.department_name;


-- ================================================================
-- 4. FULL OUTER JOIN — dono tables ki saari rows
-- ================================================================
-- MySQL me FULL JOIN NAHI hota!
-- Workaround: LEFT JOIN UNION RIGHT JOIN

SELECT
    e.name            AS employee,
    d.department_name AS department
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id

UNION

SELECT
    e.name            AS employee,
    d.department_name AS department
FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
ORDER BY department, employee;


-- ================================================================
-- 5. SELF JOIN — table khud se JOIN
-- ================================================================
-- Use: employee -> manager, category -> parent category, etc.
-- Same table ko DO ALIAS deke JOIN karte hain.

-- Har employee aur uska manager
SELECT
    e.name  AS employee,
    e.salary AS emp_salary,
    m.name  AS manager,
    m.salary AS mgr_salary
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
ORDER BY m.name, e.name;

-- Sirf jinke manager hain
SELECT
    e.name AS employee,
    m.name AS manager
FROM employees e
INNER JOIN employees m ON e.manager_id = m.id
ORDER BY manager, employee;

-- Managers aur unki team size
SELECT
    m.name          AS manager,
    COUNT(e.id)     AS team_size,
    ROUND(AVG(e.salary)) AS team_avg_salary
FROM employees m
JOIN employees e ON e.manager_id = m.id
GROUP BY m.id, m.name
ORDER BY team_size DESC;

-- Employees jo apne manager se ZYADA kamate hain (classic interview Q)
SELECT
    e.name   AS employee,
    e.salary AS emp_salary,
    m.name   AS manager,
    m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;

-- Employees jinka koi manager nahi (top level)
SELECT name, salary FROM employees WHERE manager_id IS NULL ORDER BY salary DESC;


-- ================================================================
-- 6. CROSS JOIN — har row ka har row se combination
-- ================================================================
-- Cartesian product. m rows x n rows = m*n rows
-- Galti se ON bhool jaao to yahi ho jaata hai!

SELECT
    d.department_name,
    p.project_name
FROM departments d
CROSS JOIN projects p
LIMIT 10;

-- 5 departments x 8 projects = 40 rows
SELECT COUNT(*) AS cross_join_rows FROM departments CROSS JOIN projects;


-- ================================================================
-- 7. MANY-TO-MANY JOIN (junction table)
-- ================================================================
-- employees <-> assignments <-> projects
-- Ek employee kai project me, ek project me kai employee

SELECT
    p.project_name,
    p.status,
    COUNT(a.employee_id)  AS team_size,
    SUM(a.hours)          AS total_hours,
    GROUP_CONCAT(e.name, ', ') AS team_members
FROM projects p
LEFT JOIN assignments a ON p.id = a.project_id
LEFT JOIN employees e   ON a.employee_id = e.id
GROUP BY p.id, p.project_name, p.status
ORDER BY team_size DESC;


-- ================================================================
-- 8. REAL WORLD — poora order report
-- ================================================================

SELECT
    o.id           AS order_id,
    o.order_date,
    c.name         AS customer,
    c.city,
    p.name         AS product,
    p.category,
    o.quantity,
    p.price        AS unit_price,
    o.amount       AS total
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products  p ON o.product_id  = p.id
ORDER BY o.order_date DESC;


-- ================================================================
-- INTERVIEW QUESTIONS
-- ================================================================
-- Q1. JOIN kya hai?
--     Do ya zyada tables ko common column pe jodna.
--
-- Q2. INNER vs LEFT JOIN?
--     INNER -> sirf matching rows dono taraf se
--     LEFT  -> left ki saari rows + matching right (warna NULL)
--
-- Q3. LEFT vs RIGHT JOIN?
--     Bas direction ka fark. Tables swap kar do, same result.
--
-- Q4. FULL OUTER JOIN MySQL me kaise?
--     LEFT JOIN UNION RIGHT JOIN
--
-- Q5. SELF JOIN kya hai aur kab use karte hain?
--     Table khud se JOIN. Hierarchical data ke liye (employee-manager).
--
-- Q6. CROSS JOIN kya hai?
--     Cartesian product — har row x har row. m*n rows.
--
-- Q7. Jinke paas kuch NAHI hai, unhe kaise dhoondhein?
--     LEFT JOIN + WHERE right_table.id IS NULL  (anti-join pattern)
--
-- Q8. LEFT JOIN me WHERE lagane se kya hota hai?
--     Wo INNER JOIN ban jaata hai (NULL rows filter ho jaati hain).
--     Condition ON clause me daalo.
--
-- Q9. JOIN vs Subquery — kaun better?
--     JOIN generally fast hota hai, optimizer better handle karta hai.
--     Subquery kabhi kabhi zyada readable hoti hai.
--
-- Q10. USING kya hai?
--      Jab dono tables me column ka naam SAME ho:
--      JOIN departments USING (department_id)


-- ================================================================
-- PRACTICE
-- ================================================================
-- 1.  Har employee ka naam + department name (INNER JOIN)
-- 2.  SAARE employees + department (LEFT JOIN) — NULL wale bhi
-- 3.  Jinka department assign nahi hua, unhe dhoondho
-- 4.  Har department me kitne employees (departments jinme 0 hain wo bhi)
-- 5.  Jinhone kabhi order nahi kiya wo customers
-- 6.  Har employee + uska manager (SELF JOIN)
-- 7.  Har manager ki team size
-- 8.  Employees jo manager se zyada kamate hain
-- 9.  Har project ki team (3 table JOIN)
-- 10. Products jo kabhi nahi bike
-- 11. Customer + order + product ki poori detail (3 JOIN)
-- 12. Har department ki total salary cost (LEFT JOIN + GROUP BY)
