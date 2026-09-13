-- ================================================================
-- STEP 15 — CTE (Common Table Expression)  🟡 -> 🔴
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step15_cte.sql
--
-- CTE = WITH keyword se banaya hua temporary named result.
-- Nested subquery se bahut zyada READABLE hota hai.
-- ================================================================


-- ================================================================
-- 1. BASIC CTE — tera example
-- ================================================================
--   WITH high_salary AS (
--       SELECT * FROM employees WHERE salary > 50000
--   )
--   SELECT * FROM high_salary;

WITH high_salary AS (
    SELECT id, name, salary, department_id
    FROM employees
    WHERE salary > 50000
)
SELECT * FROM high_salary ORDER BY salary DESC;

-- CTE ko normal table ki tarah use karo
WITH high_salary AS (
    SELECT id, name, salary, department_id FROM employees WHERE salary > 50000
)
SELECT
    COUNT(*)              AS count,
    ROUND(AVG(salary))    AS avg_salary,
    MAX(salary)           AS highest
FROM high_salary;

-- CTE + JOIN
WITH high_salary AS (
    SELECT id, name, salary, department_id FROM employees WHERE salary > 50000
)
SELECT h.name, h.salary, d.department_name
FROM high_salary h
JOIN departments d ON h.department_id = d.id
ORDER BY h.salary DESC;


-- ================================================================
-- 2. CTE vs SUBQUERY — readability ka fark dekho
-- ================================================================

-- SUBQUERY version (padhne me mushkil, andar se bahar padhna padta hai):
SELECT department_name, avg_salary
FROM (
    SELECT d.department_name, ROUND(AVG(e.salary)) AS avg_salary
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    GROUP BY d.department_name
) x
WHERE avg_salary > 50000
ORDER BY avg_salary DESC;

-- CTE version (upar se neeche padho — saaf):
WITH dept_avg AS (
    SELECT d.department_name, ROUND(AVG(e.salary)) AS avg_salary
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    GROUP BY d.department_name
)
SELECT department_name, avg_salary
FROM dept_avg
WHERE avg_salary > 50000
ORDER BY avg_salary DESC;


-- ================================================================
-- 3. MULTIPLE CTEs — comma se alag karo 🔥
-- ================================================================
-- Ye CTE ki asli power hai. Bade query ko chhote steps me todo.

WITH
dept_stats AS (
    SELECT
        department_id,
        COUNT(*)           AS headcount,
        ROUND(AVG(salary)) AS avg_salary,
        SUM(salary)        AS total_cost
    FROM employees
    WHERE department_id IS NOT NULL AND salary IS NOT NULL
    GROUP BY department_id
),
company_avg AS (
    SELECT ROUND(AVG(salary)) AS overall_avg
    FROM employees
    WHERE salary IS NOT NULL
),
final AS (
    SELECT
        d.department_name,
        d.location,
        s.headcount,
        s.avg_salary,
        s.total_cost,
        c.overall_avg,
        s.avg_salary - c.overall_avg AS diff_from_company
    FROM dept_stats s
    JOIN departments d ON s.department_id = d.id
    CROSS JOIN company_avg c
)
SELECT * FROM final ORDER BY diff_from_company DESC;

-- Ek aur multi-CTE example: customer segmentation
WITH
customer_totals AS (
    SELECT
        c.id,
        c.name,
        c.city,
        COUNT(o.id)                AS order_count,
        COALESCE(SUM(o.amount), 0) AS total_spent
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name, c.city
),
segmented AS (
    SELECT
        *,
        CASE
            WHEN total_spent = 0      THEN 'Never Ordered'
            WHEN total_spent > 100000 THEN 'VIP'
            WHEN total_spent > 30000  THEN 'Regular'
            ELSE 'Occasional'
        END AS segment
    FROM customer_totals
)
SELECT segment, COUNT(*) AS customers, SUM(total_spent) AS revenue
FROM segmented
GROUP BY segment
ORDER BY revenue DESC;


-- ================================================================
-- 4. CTE ek doosre ko REFER kar sakte hain
-- ================================================================
-- Baad wala CTE pehle wale ko use kar sakta hai (upar se neeche)

WITH
active_projects AS (
    SELECT id, project_name, budget
    FROM projects
    WHERE status = 'Active'
),
project_teams AS (
    -- ye upar wale CTE ko use kar raha hai
    SELECT
        ap.id,
        ap.project_name,
        ap.budget,
        COUNT(a.employee_id) AS team_size,
        SUM(a.hours)         AS total_hours
    FROM active_projects ap
    LEFT JOIN assignments a ON ap.id = a.project_id
    GROUP BY ap.id, ap.project_name, ap.budget
),
with_cost AS (
    -- ye doosre wale ko use kar raha hai
    SELECT
        *,
        ROUND(budget * 1.0 / NULLIF(team_size, 0)) AS budget_per_person
    FROM project_teams
)
SELECT * FROM with_cost ORDER BY budget DESC;


-- ================================================================
-- 5. RECURSIVE CTE — hierarchy traverse karne ke liye 🔥
-- ================================================================
-- Employee -> Manager -> Manager ka manager... poori chain
-- Syntax: WITH RECURSIVE name AS (anchor UNION ALL recursive_part)

WITH RECURSIVE org_chart AS (
    -- ANCHOR: top level (jinke manager nahi hain)
    SELECT
        id,
        name,
        manager_id,
        0 AS level,
        name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- RECURSIVE: har level ke neeche wale
    SELECT
        e.id,
        e.name,
        e.manager_id,
        oc.level + 1,
        oc.path || ' > ' || e.name
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT
    level,
    printf('%*s%s', level * 4, '', name) AS hierarchy,
    path
FROM org_chart
ORDER BY path;

-- Simple recursion: 1 se 10 tak numbers
WITH RECURSIVE numbers AS (
    SELECT 1 AS n                    -- anchor
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 10   -- recursive + STOP condition
)
SELECT n, n * n AS square FROM numbers;

-- ⚠️ Recursive CTE me STOP CONDITION zaroori hai (WHERE n < 10)
--    warna infinite loop ho jaayega.

-- Date series banao (reporting me kaam aata hai)
WITH RECURSIVE dates AS (
    SELECT '2026-01-01' AS dt
    UNION ALL
    SELECT date(dt, '+1 month') FROM dates WHERE dt < '2026-06-01'
)
SELECT dt AS month_start FROM dates;


-- ================================================================
-- 6. REAL WORLD — complete sales report
-- ================================================================

WITH
monthly_sales AS (
    SELECT
        SUBSTR(order_date, 1, 7) AS month,
        COUNT(*)                 AS orders,
        SUM(amount)              AS revenue
    FROM orders
    GROUP BY SUBSTR(order_date, 1, 7)
),
with_running AS (
    SELECT
        month,
        orders,
        revenue,
        SUM(revenue) OVER (ORDER BY month) AS running_total,
        LAG(revenue) OVER (ORDER BY month) AS prev_month
    FROM monthly_sales
)
SELECT
    month,
    orders,
    revenue,
    running_total,
    COALESCE(prev_month, 0) AS prev_month,
    CASE
        WHEN prev_month IS NULL THEN NULL
        ELSE ROUND((revenue - prev_month) * 100.0 / prev_month, 1)
    END AS growth_pct
FROM with_running
ORDER BY month;


-- ================================================================
-- INTERVIEW QUESTIONS
-- ================================================================
-- Q1. CTE kya hai?
--     WITH keyword se banaya hua temporary named result set.
--     Sirf usi ek query ke liye exist karta hai.
--
-- Q2. CTE vs Subquery?
--     CTE zyada readable, reuse ho sakta hai same query me,
--     recursion support karta hai. Performance generally same.
--
-- Q3. CTE vs Temporary Table?
--     CTE   -> memory me, query ke baad gayab, koi index nahi
--     Temp table -> disk pe, session tak rehti hai, index laga sakte ho
--
-- Q4. CTE vs VIEW?
--     CTE  -> ek query ke liye, save nahi hota
--     VIEW -> database me permanently save hota hai, baar baar use kar sakte ho
--
-- Q5. Recursive CTE kya hai?
--     Khud ko refer karne wala CTE. Hierarchical data ke liye
--     (org chart, category tree, bill of materials).
--     Anchor + UNION ALL + recursive part + stop condition.
--
-- Q6. Multiple CTE kaise likhte hain?
--     WITH a AS (...), b AS (...), c AS (...) SELECT ...
--     WITH sirf ek baar, aage comma se.
--
-- Q7. CTE me kaunse database support karte hain?
--     MySQL 8.0+, PostgreSQL, SQL Server, SQLite 3.8+, Oracle
--     MySQL 5.7 me NAHI hai — wahan subquery use karo.


-- ================================================================
-- PRACTICE
-- ================================================================
-- 1.  CTE banao high earners (60000+) ka, phir count karo
-- 2.  CTE se department-wise average nikalo, phir 50000+ filter karo
-- 3.  Do CTE banao aur unhe JOIN karo
-- 4.  Customer segmentation CTE banao (VIP/Regular/New)
-- 5.  Nested subquery wali koi query ko CTE me convert karo
-- 6.  Recursive CTE se 1-20 numbers generate karo
-- 7.  Recursive CTE se org chart banao
-- 8.  CTE se monthly revenue + growth % nikalo
-- 9.  3 CTE chain karo (ek doosre ko use karte hue)
-- 10. CTE + window function combine karo
