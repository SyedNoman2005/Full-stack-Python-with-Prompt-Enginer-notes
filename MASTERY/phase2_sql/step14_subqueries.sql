-- ================================================================
-- STEP 14 — SUBQUERIES  🔴
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step14_subqueries.sql
--
-- Subquery = query ke andar query.
-- "2nd highest salary" — ye classic interview question hai.
-- ================================================================


-- ================================================================
-- 1. SCALAR SUBQUERY — ek single value return karti hai
-- ================================================================
-- Tera example:
--   SELECT * FROM employees
--   WHERE salary > (SELECT AVG(salary) FROM employees);

-- Average se zyada kamane wale
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;

-- Average kya hai wo bhi dikhao
SELECT ROUND(AVG(salary), 2) AS company_average FROM employees;

-- SELECT clause me subquery
SELECT
    name,
    salary,
    (SELECT ROUND(AVG(salary)) FROM employees) AS company_avg,
    salary - (SELECT ROUND(AVG(salary)) FROM employees) AS difference
FROM employees
WHERE salary IS NOT NULL
ORDER BY difference DESC
LIMIT 8;


-- ================================================================
-- 2. SUBQUERY with IN — multiple values
-- ================================================================

-- Mumbai wale departments ke employees
SELECT name, department_id
FROM employees
WHERE department_id IN (
    SELECT id FROM departments WHERE location = 'Mumbai'
);

-- Jinhone Electronics khareeda
SELECT DISTINCT c.name
FROM customers c
WHERE c.id IN (
    SELECT o.customer_id
    FROM orders o
    JOIN products p ON o.product_id = p.id
    WHERE p.category = 'Electronics'
);

-- NOT IN — jinhone kabhi order nahi kiya
SELECT name, city
FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);

-- ⚠️ NOT IN + NULL KA TRAP:
-- Agar subquery me ek bhi NULL aa gaya to NOT IN KUCH BHI return nahi karega!
-- Isliye upar humne "WHERE customer_id IS NOT NULL" lagaya.
-- Safe alternative: NOT EXISTS use karo.


-- ================================================================
-- 3. EXISTS / NOT EXISTS — faster for big data
-- ================================================================
-- EXISTS pehla match milte hi ruk jaata hai — isliye fast.

-- Customers jinhone order kiya
SELECT c.name, c.city
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- Customers jinhone KABHI order nahi kiya (NULL-safe)
SELECT c.name, c.city
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- Employees jo kisi project pe hain
SELECT e.name
FROM employees e
WHERE EXISTS (SELECT 1 FROM assignments a WHERE a.employee_id = e.id)
ORDER BY e.name;

-- Employees jo kisi project pe nahi hain
SELECT e.name
FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM assignments a WHERE a.employee_id = e.id)
ORDER BY e.name;

-- NOTE: SELECT 1 likhte hain kyunki EXISTS ko value ki parwah nahi,
--       sirf row hai ya nahi ye dekhta hai.


-- ================================================================
-- 4. CORRELATED SUBQUERY — outer query pe depend karti hai
-- ================================================================
-- Har outer row ke liye subquery dobara chalti hai. Slow ho sakti hai.

-- Har employee jo apne DEPARTMENT ke average se zyada kamata hai
SELECT
    e.name,
    e.salary,
    e.department_id,
    (SELECT ROUND(AVG(e2.salary))
     FROM employees e2
     WHERE e2.department_id = e.department_id) AS dept_avg
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
)
ORDER BY e.department_id, e.salary DESC;

-- Har department ka highest paid employee
SELECT e.name, e.salary, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary = (
    SELECT MAX(e2.salary)
    FROM employees e2
    WHERE e2.department_id = e.department_id
)
ORDER BY e.salary DESC;

-- Har customer ka sabse bada order
SELECT c.name, o.amount, o.order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.amount = (
    SELECT MAX(o2.amount) FROM orders o2 WHERE o2.customer_id = c.id
)
ORDER BY o.amount DESC;


-- ================================================================
-- 5. 2ND HIGHEST SALARY  🔥 (CLASSIC INTERVIEW QUESTION)
-- ================================================================
-- Ye 5 alag tareeke se poochha jaata hai. Kam se kam 2 yaad rakho.

-- Tareeka 1: Subquery (MAX se kam ka MAX)
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Tareeka 2: LIMIT + OFFSET (simple, MySQL me sabse common)
SELECT DISTINCT salary AS second_highest
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC
LIMIT 1 OFFSET 1;

-- Tareeka 3: NOT IN
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary NOT IN (SELECT MAX(salary) FROM employees WHERE salary IS NOT NULL);

-- Tareeka 4: DENSE_RANK (Step 16 — window function, sabse professional)
SELECT salary AS second_highest
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
    WHERE salary IS NOT NULL
) ranked
WHERE rnk = 2
LIMIT 1;

-- Nth highest — general formula (3rd highest)
SELECT DISTINCT salary AS third_highest
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC
LIMIT 1 OFFSET 2;
-- Nth ke liye: OFFSET (N-1)


-- ================================================================
-- 6. HIGHEST SALARY PER DEPARTMENT  🔥 (2nd classic)
-- ================================================================

-- Tareeka 1: Correlated subquery
SELECT d.department_name, e.name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary = (
    SELECT MAX(salary) FROM employees WHERE department_id = e.department_id
)
ORDER BY e.salary DESC;

-- Tareeka 2: JOIN with derived table (generally FASTER)
SELECT d.department_name, e.name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.id
JOIN (
    SELECT department_id, MAX(salary) AS max_sal
    FROM employees
    WHERE department_id IS NOT NULL
    GROUP BY department_id
) m ON e.department_id = m.department_id AND e.salary = m.max_sal
ORDER BY e.salary DESC;


-- ================================================================
-- 7. SUBQUERY in FROM (derived table / inline view)
-- ================================================================
-- Subquery ko ek temporary table ki tarah use karo
-- ⚠️ ALIAS dena ZAROORI hai

SELECT
    dept_stats.department_id,
    d.department_name,
    dept_stats.emp_count,
    dept_stats.avg_salary
FROM (
    SELECT
        department_id,
        COUNT(*)              AS emp_count,
        ROUND(AVG(salary))    AS avg_salary
    FROM employees
    WHERE department_id IS NOT NULL AND salary IS NOT NULL
    GROUP BY department_id
) dept_stats
JOIN departments d ON dept_stats.department_id = d.id
WHERE dept_stats.avg_salary > 50000
ORDER BY dept_stats.avg_salary DESC;

-- Aggregate ke upar aggregate (ye seedhe nahi ho sakta)
SELECT ROUND(AVG(dept_avg)) AS avg_of_dept_averages
FROM (
    SELECT AVG(salary) AS dept_avg
    FROM employees
    WHERE department_id IS NOT NULL
    GROUP BY department_id
) x;


-- ================================================================
-- 8. ANY / ALL
-- ================================================================

-- ⚠️ SQLite me ANY/ALL keyword NAHI hai. MySQL me hai.
-- Neeche dono ka MySQL syntax + SQLite equivalent diya hai.

-- ANY — kisi EK se bada
--   MySQL:   WHERE salary > ANY (SELECT salary FROM employees WHERE department_id = 2)
--   Matlab:  MINIMUM se bada
--   SQLite equivalent -> > (SELECT MIN(...))
SELECT name, salary FROM employees
WHERE salary > (SELECT MIN(salary) FROM employees
                WHERE department_id = 2 AND salary IS NOT NULL)
  AND salary IS NOT NULL
ORDER BY salary LIMIT 5;

-- ALL — SABSE bada
--   MySQL:   WHERE salary > ALL (SELECT salary FROM employees WHERE department_id = 2)
--   Matlab:  MAXIMUM se bada
--   SQLite equivalent -> > (SELECT MAX(...))
SELECT name, salary FROM employees
WHERE salary > (SELECT MAX(salary) FROM employees
                WHERE department_id = 2 AND salary IS NOT NULL)
ORDER BY salary DESC;


-- ================================================================
-- 9. CLASSIC INTERVIEW PATTERNS
-- ================================================================

-- Pattern 1: Duplicate values dhoondho
SELECT city, COUNT(*) AS count
FROM employees
GROUP BY city
HAVING COUNT(*) > 1;

-- Pattern 2: Above average per group
SELECT e.name, e.salary, e.city
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE city = e.city)
ORDER BY e.city;

-- Pattern 3: Customers jinhone company average se zyada spend kiya
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
HAVING SUM(o.amount) > (
    SELECT AVG(cust_total)
    FROM (SELECT SUM(amount) AS cust_total FROM orders GROUP BY customer_id) t
)
ORDER BY total_spent DESC;

-- Pattern 4: Top 3 products by revenue
SELECT p.name, p.category, SUM(o.amount) AS revenue
FROM products p
JOIN orders o ON p.id = o.product_id
GROUP BY p.id, p.name, p.category
ORDER BY revenue DESC
LIMIT 3;


-- ================================================================
-- INTERVIEW QUESTIONS
-- ================================================================
-- Q1. Subquery kya hai?
--     Ek query ke andar doosri query. Nested query bhi kehte hain.
--
-- Q2. Correlated vs Non-correlated subquery?
--     Non-correlated -> independent, ek baar chalti hai
--     Correlated     -> outer query pe depend, har row ke liye chalti hai (slow)
--
-- Q3. IN vs EXISTS?
--     IN     -> chhoti list ke liye theek, NULL ke saath problem
--     EXISTS -> badi data ke liye fast, NULL-safe, pehla match pe ruk jaata
--
-- Q4. Subquery kahan likh sakte hain?
--     SELECT, FROM (derived table), WHERE, HAVING — sab jagah
--
-- Q5. 2nd highest salary kaise?
--     SELECT MAX(salary) FROM employees
--     WHERE salary < (SELECT MAX(salary) FROM employees);
--     Ya: ORDER BY salary DESC LIMIT 1 OFFSET 1
--
-- Q6. JOIN vs Subquery — kaun fast?
--     JOIN generally fast. Optimizer better handle karta hai.
--     Correlated subquery sabse slow ho sakti hai.
--
-- Q7. NOT IN me NULL ka kya issue hai?
--     Subquery me ek bhi NULL ho to NOT IN empty result deta hai.
--     NOT EXISTS use karo — wo NULL-safe hai.
--
-- Q8. Derived table kya hai?
--     FROM clause me likhi subquery. Alias dena zaroori hai.


-- ================================================================
-- PRACTICE (ye 8 interview me poochhe jaate hain)
-- ================================================================
-- 1.  Average se zyada salary wale employees
-- 2.  2nd highest salary (3 tareeke se)
-- 3.  3rd highest salary
-- 4.  Har department ka highest paid employee
-- 5.  Jinhone kabhi order nahi kiya (NOT EXISTS se)
-- 6.  Apne department ke average se zyada kamane wale
-- 7.  Sabse mehenga product har category me
-- 8.  Customers jinhone 50000 se zyada spend kiya
-- 9.  Employees jo company ke top 25% me hain
-- 10. Wo departments jinme koi bhi 60000+ nahi kamata
