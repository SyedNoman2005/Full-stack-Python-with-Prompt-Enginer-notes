-- ================================================================
-- STEP 13 — CASE  🔴
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step13_case.sql
--
-- CASE = SQL ka if-else.
-- Data Analyst + Backend dono me bahut use hota hai.
-- ================================================================


-- ================================================================
-- 1. BASIC CASE — tera example
-- ================================================================
--   SELECT name, salary,
--   CASE
--       WHEN salary >= 50000 THEN 'High'
--       WHEN salary >= 30000 THEN 'Medium'
--       ELSE 'Low'
--   END AS category
--   FROM employees;

SELECT
    name,
    salary,
    CASE
        WHEN salary >= 50000 THEN 'High'
        WHEN salary >= 30000 THEN 'Medium'
        ELSE 'Low'
    END AS category
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC;

-- ⚠️ ORDER MATTERS! Pehla matching WHEN jeetta hai.
-- Agar 'Medium' wali line upar likh dete, to 60000 bhi 'Medium' ho jaati.


-- ================================================================
-- 2. NULL HANDLING ke saath CASE
-- ================================================================

SELECT
    name,
    salary,
    CASE
        WHEN salary IS NULL   THEN 'Not Disclosed'
        WHEN salary >= 80000  THEN 'Senior Level'
        WHEN salary >= 50000  THEN 'Mid Level'
        WHEN salary >= 35000  THEN 'Junior Level'
        ELSE 'Entry Level'
    END AS level
FROM employees
ORDER BY COALESCE(salary, 0) DESC;


-- ================================================================
-- 3. SIMPLE CASE (equality check ke liye)
-- ================================================================
-- Do form hote hain:
--   Searched CASE: CASE WHEN condition THEN ...   (flexible)
--   Simple CASE:   CASE column WHEN value THEN ... (sirf equality)

SELECT
    project_name,
    status,
    CASE status
        WHEN 'Active'    THEN '🟢 Chal raha hai'
        WHEN 'Completed' THEN '✅ Ho gaya'
        WHEN 'On Hold'   THEN '⏸️  Ruka hua'
        WHEN 'Planning'  THEN '📋 Plan ho raha'
        ELSE '❓ Unknown'
    END AS status_label
FROM projects
ORDER BY status;


-- ================================================================
-- 4. CASE + AGGREGATE (conditional aggregation) 🔥
-- ================================================================
-- Ye bahut powerful pattern hai — interview me impress karta hai

SELECT
    city,
    COUNT(*)                                              AS total,
    SUM(CASE WHEN salary >= 60000 THEN 1 ELSE 0 END)      AS high_earners,
    SUM(CASE WHEN salary BETWEEN 40000 AND 59999 THEN 1 ELSE 0 END) AS mid_earners,
    SUM(CASE WHEN salary < 40000 THEN 1 ELSE 0 END)       AS low_earners,
    SUM(CASE WHEN salary IS NULL THEN 1 ELSE 0 END)       AS no_salary_data
FROM employees
GROUP BY city
ORDER BY total DESC;

-- COUNT with CASE (NULL count nahi hota, isliye ELSE NULL)
SELECT
    d.department_name,
    COUNT(*)                                               AS total,
    COUNT(CASE WHEN e.salary > 50000 THEN 1 END)          AS above_50k,
    ROUND(AVG(CASE WHEN e.salary > 50000 THEN e.salary END)) AS avg_of_high
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.department_name;


-- ================================================================
-- 5. PIVOT TABLE banao CASE se 🔥
-- ================================================================
-- Rows ko columns me badalna — Excel pivot jaisa
-- MySQL me PIVOT nahi hota, CASE se karte hain

SELECT
    d.department_name,
    SUM(CASE WHEN e.city = 'Hyderabad' THEN 1 ELSE 0 END) AS hyderabad,
    SUM(CASE WHEN e.city = 'Mumbai'    THEN 1 ELSE 0 END) AS mumbai,
    SUM(CASE WHEN e.city = 'Delhi'     THEN 1 ELSE 0 END) AS delhi,
    SUM(CASE WHEN e.city = 'Bangalore' THEN 1 ELSE 0 END) AS bangalore,
    COUNT(*) AS total
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.department_name
ORDER BY total DESC;

-- Monthly revenue pivot
SELECT
    c.name AS customer,
    SUM(CASE WHEN SUBSTR(o.order_date,1,7) = '2026-01' THEN o.amount ELSE 0 END) AS jan,
    SUM(CASE WHEN SUBSTR(o.order_date,1,7) = '2026-02' THEN o.amount ELSE 0 END) AS feb,
    SUM(CASE WHEN SUBSTR(o.order_date,1,7) = '2026-03' THEN o.amount ELSE 0 END) AS mar,
    SUM(CASE WHEN SUBSTR(o.order_date,1,7) = '2026-04' THEN o.amount ELSE 0 END) AS apr,
    SUM(o.amount) AS total
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total DESC;


-- ================================================================
-- 6. CASE in ORDER BY (custom sorting)
-- ================================================================
-- Status ko apni marzi ke order me sort karo (alphabetical nahi)

SELECT project_name, status, budget
FROM projects
ORDER BY
    CASE status
        WHEN 'Active'    THEN 1
        WHEN 'Planning'  THEN 2
        WHEN 'On Hold'   THEN 3
        WHEN 'Completed' THEN 4
        ELSE 5
    END,
    budget DESC;


-- ================================================================
-- 7. CASE in UPDATE (bulk conditional update)
-- ================================================================

DROP TABLE IF EXISTS temp_emp;
CREATE TABLE temp_emp AS SELECT id, name, salary FROM employees WHERE salary IS NOT NULL;

-- Alag alag raise alag alag salary band ko
UPDATE temp_emp
SET salary = CASE
    WHEN salary < 40000  THEN salary * 1.15   -- 15% raise
    WHEN salary < 60000  THEN salary * 1.10   -- 10% raise
    ELSE salary * 1.05                        -- 5% raise
END;

SELECT id, name, ROUND(salary) AS new_salary FROM temp_emp ORDER BY new_salary DESC LIMIT 8;

DROP TABLE temp_emp;


-- ================================================================
-- 8. CASE ke ALTERNATIVES (chhote kaam ke liye)
-- ================================================================

-- COALESCE — pehli non-NULL value
SELECT name, COALESCE(salary, 0) AS salary FROM employees WHERE salary IS NULL;

-- NULLIF — do values equal hon to NULL do
-- Divide by zero se bachne ke liye classic use:
SELECT
    name,
    salary,
    salary / NULLIF(0, 0) AS safe_divide   -- error ki jagah NULL
FROM employees LIMIT 2;

-- IIF (SQLite/SQL Server) — simple 2-way condition
SELECT name, salary, IIF(salary > 50000, 'High', 'Normal') AS band
FROM employees WHERE salary IS NOT NULL LIMIT 5;
-- MySQL me: IF(salary > 50000, 'High', 'Normal')


-- ================================================================
-- 9. REAL WORLD — employee scorecard
-- ================================================================

SELECT
    e.name,
    d.department_name AS dept,
    e.salary,
    CASE
        WHEN e.salary IS NULL THEN 'N/A'
        WHEN e.salary >= 80000 THEN 'A'
        WHEN e.salary >= 55000 THEN 'B'
        WHEN e.salary >= 40000 THEN 'C'
        ELSE 'D'
    END AS salary_grade,
    CASE
        WHEN e.hire_date < '2021-01-01' THEN 'Veteran (5+ yrs)'
        WHEN e.hire_date < '2024-01-01' THEN 'Experienced (2-5 yrs)'
        ELSE 'New (< 2 yrs)'
    END AS tenure,
    CASE WHEN e.manager_id IS NULL THEN 'Yes' ELSE 'No' END AS is_leader
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id
ORDER BY COALESCE(e.salary, 0) DESC;


-- ================================================================
-- INTERVIEW QUESTIONS
-- ================================================================
-- Q1. CASE kya hai?
--     SQL ka if-else. Condition ke hisaab se alag value return karta hai.
--
-- Q2. Simple CASE vs Searched CASE?
--     Simple:   CASE column WHEN value THEN ...    (sirf equality)
--     Searched: CASE WHEN condition THEN ...       (koi bhi condition)
--
-- Q3. ELSE na likhein to?
--     Koi condition match na ho to NULL return hota hai.
--
-- Q4. CASE kahan kahan use kar sakte hain?
--     SELECT, WHERE, ORDER BY, GROUP BY, HAVING, UPDATE — sab jagah.
--
-- Q5. Pivot table kaise banate hain SQL me?
--     CASE + aggregate (SUM/COUNT) + GROUP BY
--
-- Q6. CASE ka order matter karta hai?
--     HAAN. Pehla matching WHEN chalta hai, baaki skip.
--
-- Q7. COALESCE vs CASE?
--     COALESCE sirf NULL check ke liye (chhota).
--     CASE koi bhi condition handle karta hai.


-- ================================================================
-- PRACTICE
-- ================================================================
-- 1.  Salary ko High/Medium/Low me classify karo
-- 2.  Products ko price ke hisaab se Cheap/Moderate/Expensive
-- 3.  Stock 0 ho to 'Out of Stock', warna 'Available'
-- 4.  Har city me high/low earners count karo (conditional aggregation)
-- 5.  Department x City ka pivot table banao
-- 6.  Orders ko amount ke hisaab se Small/Medium/Large
-- 7.  Project status ko custom order me sort karo
-- 8.  Employees ko tenure ke hisaab se categorize karo
-- 9.  NULL salary ko 'Not Disclosed' dikhao
-- 10. Har department me male/female ratio (agar gender column hota)
