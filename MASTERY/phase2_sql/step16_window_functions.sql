-- ================================================================
-- STEP 16 — WINDOW FUNCTIONS  🔴
-- ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, OVER, PARTITION BY
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step16_window_functions.sql
--
-- Data Analyst / Data Scientist ke liye SABSE POWERFUL topic.
-- Backend me bhi leaderboard, ranking, running total me use hota hai.
--
-- KEY IDEA:
--   GROUP BY  -> rows ko SQUEEZE kar deta hai (10 rows -> 3 rows)
--   WINDOW    -> saari rows RAKHTA hai, saath me calculation add karta hai
-- ================================================================


-- ================================================================
-- 1. GROUP BY vs WINDOW — fark samjho
-- ================================================================

-- GROUP BY: 20 rows -> 4 rows (squeeze ho gaya)
SELECT city, ROUND(AVG(salary)) AS avg_salary
FROM employees WHERE salary IS NOT NULL
GROUP BY city;

-- WINDOW: 18 rows hi rahengi, har row ke saath avg bhi aayega
SELECT
    name,
    city,
    salary,
    ROUND(AVG(salary) OVER (PARTITION BY city)) AS city_avg,
    salary - ROUND(AVG(salary) OVER (PARTITION BY city)) AS diff_from_city_avg
FROM employees
WHERE salary IS NOT NULL
ORDER BY city, salary DESC;

-- ^^ Ye GROUP BY se NAHI ho sakta. Yahi window function ki power hai.


-- ================================================================
-- 2. OVER() — basic syntax
-- ================================================================
-- SYNTAX:
--   function() OVER (PARTITION BY col ORDER BY col)
--
--   PARTITION BY -> groups banao (GROUP BY jaisa, par rows nahi squeeze hoti)
--   ORDER BY     -> group ke andar order

-- Bina PARTITION — poori table ek window
SELECT
    name,
    salary,
    ROUND(AVG(salary) OVER ())         AS company_avg,
    MAX(salary) OVER ()                AS company_max,
    COUNT(*) OVER ()                   AS total_employees
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC
LIMIT 8;


-- ================================================================
-- 3. RANKING: ROW_NUMBER vs RANK vs DENSE_RANK  🔥
-- ================================================================
-- Ye teeno ka fark 100% interview me poochha jaata hai.
--
--   ROW_NUMBER() -> 1,2,3,4,5    hamesha unique, tie pe bhi alag
--   RANK()       -> 1,2,2,4,5    tie pe same rank, phir GAP
--   DENSE_RANK() -> 1,2,2,3,4    tie pe same rank, koi GAP nahi

-- Tera example:
--   SELECT name, salary, RANK() OVER (ORDER BY salary DESC) AS ranking
--   FROM employees;

SELECT
    name,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
    RANK()       OVER (ORDER BY salary DESC) AS rank_val,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank_val
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC;

-- Tie banake fark dikhate hain
DROP TABLE IF EXISTS tie_demo;
CREATE TABLE tie_demo (name TEXT, score INTEGER);
INSERT INTO tie_demo VALUES
 ('A', 100), ('B', 90), ('C', 90), ('D', 90), ('E', 80), ('F', 70);

SELECT
    name,
    score,
    ROW_NUMBER() OVER (ORDER BY score DESC) AS row_number,
    RANK()       OVER (ORDER BY score DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM tie_demo;

-- ^^ DEKHO:
--    B, C, D sabka score 90 hai
--    ROW_NUMBER -> 2, 3, 4  (zabardasti alag)
--    RANK       -> 2, 2, 2, phir 5  (GAP hai — 3 aur 4 skip)
--    DENSE_RANK -> 2, 2, 2, phir 3  (koi GAP nahi)

DROP TABLE tie_demo;


-- ================================================================
-- 4. PARTITION BY — har group ke andar ranking 🔥
-- ================================================================

-- Har city me salary ranking
SELECT
    city,
    name,
    salary,
    RANK() OVER (PARTITION BY city ORDER BY salary DESC) AS rank_in_city
FROM employees
WHERE salary IS NOT NULL
ORDER BY city, rank_in_city;

-- Har department ka TOP 2 earner (bahut common requirement)
WITH ranked AS (
    SELECT
        d.department_name,
        e.name,
        e.salary,
        DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS rnk
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    WHERE e.salary IS NOT NULL
)
SELECT * FROM ranked WHERE rnk <= 2 ORDER BY department_name, rnk;

-- 2nd highest salary — window function tareeka (sabse professional)
WITH ranked AS (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees WHERE salary IS NOT NULL
)
SELECT DISTINCT salary AS second_highest FROM ranked WHERE rnk = 2;


-- ================================================================
-- 5. LAG / LEAD — pichli aur agli row dekho 🔥
-- ================================================================
-- LAG  -> PICHLI row ki value
-- LEAD -> AGLI row ki value
-- Month-over-month growth ke liye perfect.

-- Monthly revenue with growth
WITH monthly AS (
    SELECT SUBSTR(order_date, 1, 7) AS month, SUM(amount) AS revenue
    FROM orders GROUP BY SUBSTR(order_date, 1, 7)
)
SELECT
    month,
    revenue,
    LAG(revenue)  OVER (ORDER BY month) AS prev_month,
    LEAD(revenue) OVER (ORDER BY month) AS next_month,
    revenue - LAG(revenue) OVER (ORDER BY month) AS change,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
        / LAG(revenue) OVER (ORDER BY month), 1
    ) AS growth_pct
FROM monthly
ORDER BY month;

-- LAG with DEFAULT value (NULL ki jagah)
-- LAG(column, offset, default_value)
WITH monthly AS (
    SELECT SUBSTR(order_date, 1, 7) AS month, SUM(amount) AS revenue
    FROM orders GROUP BY SUBSTR(order_date, 1, 7)
)
SELECT
    month,
    revenue,
    LAG(revenue, 1, 0) OVER (ORDER BY month) AS prev_month_or_zero
FROM monthly ORDER BY month;

-- Salary gap between consecutive employees
SELECT
    name,
    salary,
    LAG(salary) OVER (ORDER BY salary DESC) AS next_higher,
    LAG(salary) OVER (ORDER BY salary DESC) - salary AS gap
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC;


-- ================================================================
-- 6. RUNNING TOTAL / CUMULATIVE SUM 🔥
-- ================================================================

SELECT
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date, id) AS running_total,
    ROUND(AVG(amount) OVER (ORDER BY order_date, id)) AS running_avg,
    COUNT(*) OVER (ORDER BY order_date, id) AS order_number
FROM orders
ORDER BY order_date, id;

-- Running total per customer (PARTITION ke saath)
SELECT
    c.name AS customer,
    o.order_date,
    o.amount,
    SUM(o.amount) OVER (PARTITION BY c.id ORDER BY o.order_date, o.id) AS customer_running_total
FROM orders o
JOIN customers c ON o.customer_id = c.id
ORDER BY c.name, o.order_date;


-- ================================================================
-- 7. FIRST_VALUE / LAST_VALUE / NTH_VALUE
-- ================================================================

SELECT
    city,
    name,
    salary,
    FIRST_VALUE(name) OVER (PARTITION BY city ORDER BY salary DESC) AS top_earner_in_city,
    FIRST_VALUE(salary) OVER (PARTITION BY city ORDER BY salary DESC) AS top_salary_in_city
FROM employees
WHERE salary IS NOT NULL
ORDER BY city, salary DESC;


-- ================================================================
-- 8. NTILE — buckets me baato (quartiles, percentiles)
-- ================================================================

SELECT
    name,
    salary,
    NTILE(4) OVER (ORDER BY salary DESC) AS quartile,
    CASE NTILE(4) OVER (ORDER BY salary DESC)
        WHEN 1 THEN 'Top 25%'
        WHEN 2 THEN 'Upper Mid'
        WHEN 3 THEN 'Lower Mid'
        ELSE 'Bottom 25%'
    END AS band
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC;


-- ================================================================
-- 9. PERCENT_RANK / CUME_DIST
-- ================================================================

SELECT
    name,
    salary,
    ROUND(PERCENT_RANK() OVER (ORDER BY salary) * 100, 1) AS percentile,
    ROUND(CUME_DIST()    OVER (ORDER BY salary) * 100, 1) AS cumulative_pct
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC;


-- ================================================================
-- 10. COMPLETE ANALYTICS DASHBOARD
-- ================================================================

WITH emp_analytics AS (
    SELECT
        e.name,
        d.department_name AS dept,
        e.city,
        e.salary,
        RANK()       OVER (ORDER BY e.salary DESC)                        AS company_rank,
        RANK()       OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS dept_rank,
        ROUND(AVG(e.salary) OVER (PARTITION BY e.department_id))          AS dept_avg,
        ROUND(AVG(e.salary) OVER ())                                      AS company_avg,
        NTILE(4)     OVER (ORDER BY e.salary DESC)                        AS quartile
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    WHERE e.salary IS NOT NULL
)
SELECT
    company_rank,
    name,
    dept,
    salary,
    dept_rank,
    dept_avg,
    salary - dept_avg AS vs_dept,
    salary - company_avg AS vs_company,
    quartile
FROM emp_analytics
ORDER BY company_rank;


-- ================================================================
-- INTERVIEW QUESTIONS
-- ================================================================
-- Q1. Window function kya hai?
--     Rows ke ek "window" (set) pe calculation karta hai
--     BINA rows ko collapse kiye. GROUP BY rows squeeze karta hai.
--
-- Q2. ROW_NUMBER vs RANK vs DENSE_RANK? (MOST ASKED)
--     Scores: 100, 90, 90, 80
--     ROW_NUMBER -> 1, 2, 3, 4     (hamesha unique)
--     RANK       -> 1, 2, 2, 4     (tie pe gap)
--     DENSE_RANK -> 1, 2, 2, 3     (tie pe gap nahi)
--
-- Q3. PARTITION BY vs GROUP BY?
--     GROUP BY     -> rows collapse, ek row per group
--     PARTITION BY -> rows same rehti hain, bas window define hoti hai
--
-- Q4. LAG vs LEAD?
--     LAG  -> pichli row ki value
--     LEAD -> agli row ki value
--     Growth %, trend analysis me use hote hain
--
-- Q5. Running total kaise?
--     SUM(amount) OVER (ORDER BY date)
--
-- Q6. Top N per group kaise?
--     ROW_NUMBER()/RANK() PARTITION BY ke saath, phir CTE me WHERE rnk <= N
--     (Window function WHERE me directly nahi likh sakte!)
--
-- Q7. Window function WHERE me kyun nahi chalta?
--     Window functions SELECT ke baad evaluate hote hain, WHERE se pehle nahi.
--     Isliye CTE ya subquery me wrap karo.
--
-- Q8. NTILE kya karta hai?
--     Rows ko N equal buckets me baant deta hai. Quartile/percentile ke liye.
--
-- Q9. Kaun se DB support karte hain?
--     MySQL 8.0+, PostgreSQL, SQL Server, Oracle, SQLite 3.25+
--     MySQL 5.7 me NAHI hai.


-- ================================================================
-- PRACTICE
-- ================================================================
-- 1.  Salary ke hisaab se ranking do (RANK)
-- 2.  ROW_NUMBER, RANK, DENSE_RANK ka fark dikhao ek query me
-- 3.  Har city me salary ranking (PARTITION BY)
-- 4.  Har department ka top 2 earner nikalo
-- 5.  2nd highest salary window function se
-- 6.  Monthly revenue ka running total
-- 7.  Month-over-month growth % (LAG se)
-- 8.  Har row ke saath company average dikhao
-- 9.  Employees ko 4 quartiles me baanto (NTILE)
-- 10. Har customer ka running total spending
-- 11. Har department ka top earner FIRST_VALUE se
-- 12. Salary percentile nikalo har employee ka
