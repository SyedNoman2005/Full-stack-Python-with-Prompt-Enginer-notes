-- ================================================================
-- PHASE 2 — SQL PRACTICE SOLUTIONS (Steps 9-17)
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/solutions/all_solutions.sql
--
-- ⚠️  PEHLE KHUD LIKHO. Atak jao tabhi yahan dekho.
-- ================================================================


-- ================================================================
-- STEP 9 — BASICS
-- ================================================================

-- 1. students table banao
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    marks INTEGER,
    grade TEXT
);

-- 2. 5 students insert
INSERT INTO students (id, name, marks, grade) VALUES
 (1, 'Noman', 85, 'B'), (2, 'Sara', 92, 'A'), (3, 'Ali', 67, 'C'),
 (4, 'Zoya', 38, 'F'),  (5, 'Imran', 74, 'B');

-- 3. Saare students
SELECT * FROM students;

-- 4. Sirf name aur marks
SELECT name, marks FROM students;

-- 5. Marks descending
SELECT name, marks FROM students ORDER BY marks DESC;

-- 6. Top 3
SELECT name, marks FROM students ORDER BY marks DESC LIMIT 3;

-- 7. Ek student ke marks update
UPDATE students SET marks = 90, grade = 'A' WHERE id = 1;
SELECT * FROM students WHERE id = 1;

-- 8. Sabke marks me 5 add
UPDATE students SET marks = marks + 5;
SELECT name, marks FROM students;

-- 9. 40 se kam wale delete
DELETE FROM students WHERE marks < 40;
SELECT * FROM students;

-- 10. Top 5 salary
SELECT name, salary FROM employees
WHERE salary IS NOT NULL ORDER BY salary DESC LIMIT 5;

-- 11. DISTINCT cities
SELECT DISTINCT city FROM employees ORDER BY city;

-- 12. Annual salary
SELECT name, salary, salary * 12 AS annual FROM employees
WHERE salary IS NOT NULL ORDER BY annual DESC;

DROP TABLE students;


-- ================================================================
-- STEP 10 — FILTERING
-- ================================================================

-- 1. 50000+ salary
SELECT name, salary FROM employees WHERE salary > 50000 ORDER BY salary DESC;

-- 2. Hyderabad ya Bangalore (IN)
SELECT name, city FROM employees WHERE city IN ('Hyderabad', 'Bangalore');

-- 3. 40000-60000 (BETWEEN)
SELECT name, salary FROM employees WHERE salary BETWEEN 40000 AND 60000;

-- 4. 'S' se shuru
SELECT name FROM employees WHERE name LIKE 'S%';

-- 5. Email me 'techcorp'
SELECT name, email FROM employees WHERE email LIKE '%techcorp%' LIMIT 5;

-- 6. Salary NULL
SELECT id, name FROM employees WHERE salary IS NULL;

-- 7. Department assign nahi
SELECT id, name FROM employees WHERE department_id IS NULL;

-- 8. Mumbai + 50000+ (AND)
SELECT name, salary FROM employees WHERE city = 'Mumbai' AND salary > 50000;

-- 9. Delhi ya Mumbai, par 60000+ (BRACKETS zaroori)
SELECT name, city, salary FROM employees
WHERE (city = 'Delhi' OR city = 'Mumbai') AND salary > 60000;

-- 10. 2023 me join hue
SELECT name, hire_date FROM employees
WHERE hire_date BETWEEN '2023-01-01' AND '2023-12-31' ORDER BY hire_date;

-- 11. 6 character ke naam
SELECT name FROM employees WHERE name LIKE '______';

-- 12. IT/HR me nahi
SELECT name FROM employees
WHERE department_id NOT IN (SELECT id FROM departments WHERE department_name IN ('IT','HR'))
   OR department_id IS NULL;


-- ================================================================
-- STEP 11 — AGGREGATES
-- ================================================================

-- 1. Total employees
SELECT COUNT(*) AS total FROM employees;

-- 2. Average salary
SELECT ROUND(AVG(salary), 2) AS avg_salary FROM employees;

-- 3. Max aur min
SELECT MAX(salary) AS highest, MIN(salary) AS lowest FROM employees;

-- 4. Har city me kitne
SELECT city, COUNT(*) AS count FROM employees GROUP BY city ORDER BY count DESC;

-- 5. Har department ki average
SELECT d.department_name, ROUND(AVG(e.salary)) AS avg_salary
FROM employees e JOIN departments d ON e.department_id = d.id
GROUP BY d.department_name ORDER BY avg_salary DESC;

-- 6. Cities with 2+ employees
SELECT city, COUNT(*) AS count FROM employees GROUP BY city HAVING COUNT(*) > 2;

-- 7. Departments with total salary > 200000
SELECT d.department_name, SUM(e.salary) AS total
FROM employees e JOIN departments d ON e.department_id = d.id
GROUP BY d.department_name HAVING SUM(e.salary) > 200000;

-- 8. Har customer ke orders
SELECT c.name, COUNT(o.id) AS orders FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name ORDER BY orders DESC;

-- 9. Category ka total stock
SELECT category, SUM(stock) AS total_stock FROM products GROUP BY category;

-- 10. Monthly revenue
SELECT SUBSTR(order_date,1,7) AS month, SUM(amount) AS revenue
FROM orders GROUP BY month ORDER BY month;

-- 11. 2+ projects wale employees
SELECT e.name, COUNT(a.project_id) AS projects FROM employees e
JOIN assignments a ON e.id = a.employee_id
GROUP BY e.id, e.name HAVING COUNT(a.project_id) > 1 ORDER BY projects DESC;

-- 12. Har city me 50000+ kitne (conditional aggregation)
SELECT city, COUNT(*) AS total,
       SUM(CASE WHEN salary > 50000 THEN 1 ELSE 0 END) AS above_50k
FROM employees GROUP BY city;


-- ================================================================
-- STEP 12 — JOINS
-- ================================================================

-- 1. Employee + department (INNER)
SELECT e.name, d.department_name FROM employees e
JOIN departments d ON e.department_id = d.id ORDER BY d.department_name;

-- 2. SAARE employees + department (LEFT)
SELECT e.name, COALESCE(d.department_name,'Not Assigned') AS dept
FROM employees e LEFT JOIN departments d ON e.department_id = d.id ORDER BY e.id;

-- 3. Department assign nahi hua
SELECT e.name FROM employees e
LEFT JOIN departments d ON e.department_id = d.id WHERE d.id IS NULL;

-- 4. Har department me kitne (0 wale bhi)
SELECT d.department_name, COUNT(e.id) AS headcount FROM departments d
LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.department_name ORDER BY headcount DESC;

-- 5. Jinhone kabhi order nahi kiya (ANTI-JOIN)
SELECT c.name, c.city FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id WHERE o.id IS NULL;

-- 6. Employee + manager (SELF JOIN)
SELECT e.name AS employee, COALESCE(m.name,'No Manager') AS manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.id ORDER BY manager;

-- 7. Manager ki team size
SELECT m.name AS manager, COUNT(e.id) AS team_size FROM employees m
JOIN employees e ON e.manager_id = m.id GROUP BY m.id, m.name ORDER BY team_size DESC;

-- 8. Manager se zyada kamane wale
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS mgr_salary
FROM employees e JOIN employees m ON e.manager_id = m.id WHERE e.salary > m.salary;

-- 9. Har project ki team (3 JOIN)
SELECT p.project_name, COUNT(a.employee_id) AS team_size,
       GROUP_CONCAT(e.name, ', ') AS members
FROM projects p LEFT JOIN assignments a ON p.id = a.project_id
LEFT JOIN employees e ON a.employee_id = e.id
GROUP BY p.id, p.project_name ORDER BY team_size DESC;

-- 10. Products jo kabhi nahi bike
SELECT p.name, p.category, p.price FROM products p
LEFT JOIN orders o ON p.id = o.product_id WHERE o.id IS NULL;

-- 11. Customer + order + product
SELECT c.name AS customer, p.name AS product, o.quantity, o.amount, o.order_date
FROM orders o JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id ORDER BY o.order_date DESC;

-- 12. Department ki total cost
SELECT d.department_name, COUNT(e.id) AS headcount,
       COALESCE(SUM(e.salary),0) AS monthly_cost
FROM departments d LEFT JOIN employees e ON d.id = e.department_id
GROUP BY d.id, d.department_name ORDER BY monthly_cost DESC;


-- ================================================================
-- STEP 13 — CASE
-- ================================================================

-- 1. High/Medium/Low
SELECT name, salary,
  CASE WHEN salary >= 50000 THEN 'High'
       WHEN salary >= 30000 THEN 'Medium'
       ELSE 'Low' END AS category
FROM employees WHERE salary IS NOT NULL ORDER BY salary DESC;

-- 2. Product price category
SELECT name, price,
  CASE WHEN price >= 20000 THEN 'Expensive'
       WHEN price >= 3000  THEN 'Moderate'
       ELSE 'Cheap' END AS price_band
FROM products ORDER BY price DESC;

-- 3. Stock status
SELECT name, stock, CASE WHEN stock = 0 THEN 'Out of Stock' ELSE 'Available' END AS status
FROM products ORDER BY stock;

-- 4. High/low earners per city
SELECT city,
  SUM(CASE WHEN salary > 50000 THEN 1 ELSE 0 END) AS high,
  SUM(CASE WHEN salary <= 50000 THEN 1 ELSE 0 END) AS low
FROM employees WHERE salary IS NOT NULL GROUP BY city;

-- 5. Department x City pivot
SELECT d.department_name,
  SUM(CASE WHEN e.city='Hyderabad' THEN 1 ELSE 0 END) AS hyderabad,
  SUM(CASE WHEN e.city='Mumbai'    THEN 1 ELSE 0 END) AS mumbai,
  SUM(CASE WHEN e.city='Delhi'     THEN 1 ELSE 0 END) AS delhi,
  SUM(CASE WHEN e.city='Bangalore' THEN 1 ELSE 0 END) AS bangalore
FROM employees e JOIN departments d ON e.department_id = d.id
GROUP BY d.department_name;

-- 6. Order size
SELECT id, amount,
  CASE WHEN amount >= 50000 THEN 'Large'
       WHEN amount >= 10000 THEN 'Medium'
       ELSE 'Small' END AS size
FROM orders ORDER BY amount DESC;

-- 7. Custom status sort
SELECT project_name, status FROM projects
ORDER BY CASE status WHEN 'Active' THEN 1 WHEN 'Planning' THEN 2
                     WHEN 'On Hold' THEN 3 ELSE 4 END;

-- 8. Tenure category
SELECT name, hire_date,
  CASE WHEN hire_date < '2021-01-01' THEN 'Veteran'
       WHEN hire_date < '2024-01-01' THEN 'Experienced'
       ELSE 'New' END AS tenure
FROM employees ORDER BY hire_date;

-- 9. NULL salary
SELECT name, CASE WHEN salary IS NULL THEN 'Not Disclosed'
                  ELSE CAST(salary AS TEXT) END AS salary_display
FROM employees;


-- ================================================================
-- STEP 14 — SUBQUERIES
-- ================================================================

-- 1. Average se zyada
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees) ORDER BY salary DESC;

-- 2. 2nd highest (3 tareeke)
SELECT MAX(salary) AS method1 FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

SELECT DISTINCT salary AS method2 FROM employees
WHERE salary IS NOT NULL ORDER BY salary DESC LIMIT 1 OFFSET 1;

SELECT salary AS method3 FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) rnk
  FROM employees WHERE salary IS NOT NULL) x WHERE rnk = 2 LIMIT 1;

-- 3. 3rd highest
SELECT DISTINCT salary AS third FROM employees
WHERE salary IS NOT NULL ORDER BY salary DESC LIMIT 1 OFFSET 2;

-- 4. Har department ka top earner
SELECT d.department_name, e.name, e.salary
FROM employees e JOIN departments d ON e.department_id = d.id
WHERE e.salary = (SELECT MAX(salary) FROM employees WHERE department_id = e.department_id)
ORDER BY e.salary DESC;

-- 5. Kabhi order nahi kiya (NOT EXISTS)
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- 6. Department average se zyada
SELECT e.name, e.salary FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id)
ORDER BY e.salary DESC;

-- 7. Har category ka sabse mehenga product
SELECT category, name, price FROM products p
WHERE price = (SELECT MAX(price) FROM products WHERE category = p.category);

-- 8. 50000+ spend karne wale customers
SELECT c.name, SUM(o.amount) AS total FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name HAVING SUM(o.amount) > 50000 ORDER BY total DESC;

-- 10. Departments jinme koi 60000+ nahi
SELECT d.department_name FROM departments d
WHERE NOT EXISTS (SELECT 1 FROM employees e
                  WHERE e.department_id = d.id AND e.salary > 60000);


-- ================================================================
-- STEP 15 — CTE
-- ================================================================

-- 1. High earners CTE
WITH high_earners AS (SELECT * FROM employees WHERE salary > 60000)
SELECT COUNT(*) AS count, ROUND(AVG(salary)) AS avg FROM high_earners;

-- 2. Department average, 50000+ filter
WITH dept_avg AS (
  SELECT d.department_name, ROUND(AVG(e.salary)) AS avg_salary
  FROM employees e JOIN departments d ON e.department_id = d.id
  GROUP BY d.department_name)
SELECT * FROM dept_avg WHERE avg_salary > 50000 ORDER BY avg_salary DESC;

-- 3. Do CTE JOIN
WITH
dept_counts AS (SELECT department_id, COUNT(*) AS cnt FROM employees
                WHERE department_id IS NOT NULL GROUP BY department_id),
dept_sums   AS (SELECT department_id, SUM(salary) AS total FROM employees
                WHERE department_id IS NOT NULL GROUP BY department_id)
SELECT d.department_name, c.cnt, s.total
FROM dept_counts c JOIN dept_sums s ON c.department_id = s.department_id
JOIN departments d ON c.department_id = d.id ORDER BY s.total DESC;

-- 4. Customer segmentation
WITH totals AS (
  SELECT c.name, COALESCE(SUM(o.amount),0) AS spent
  FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name)
SELECT name, spent,
  CASE WHEN spent = 0 THEN 'Never Ordered'
       WHEN spent > 100000 THEN 'VIP'
       WHEN spent > 30000 THEN 'Regular' ELSE 'Occasional' END AS segment
FROM totals ORDER BY spent DESC;

-- 6. Recursive 1-20
WITH RECURSIVE nums AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM nums WHERE n < 20)
SELECT n, n*n AS square FROM nums;

-- 7. Org chart
WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 0 AS lvl FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, o.lvl+1 FROM employees e JOIN org o ON e.manager_id = o.id)
SELECT lvl, printf('%*s%s', lvl*3, '', name) AS chart FROM org ORDER BY lvl, name;

-- 8. Monthly revenue + growth
WITH monthly AS (
  SELECT SUBSTR(order_date,1,7) AS month, SUM(amount) AS revenue
  FROM orders GROUP BY month)
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev,
  ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
        / LAG(revenue) OVER (ORDER BY month), 1) AS growth_pct
FROM monthly ORDER BY month;


-- ================================================================
-- STEP 16 — WINDOW FUNCTIONS
-- ================================================================

-- 1-2. Teeno ranking functions
SELECT name, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
  RANK()       OVER (ORDER BY salary DESC) AS rank_val,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank_val
FROM employees WHERE salary IS NOT NULL;

-- 3. City-wise ranking
SELECT city, name, salary,
  RANK() OVER (PARTITION BY city ORDER BY salary DESC) AS rank_in_city
FROM employees WHERE salary IS NOT NULL ORDER BY city, rank_in_city;

-- 4. Top 2 per department
WITH ranked AS (
  SELECT d.department_name, e.name, e.salary,
    DENSE_RANK() OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) rnk
  FROM employees e JOIN departments d ON e.department_id = d.id
  WHERE e.salary IS NOT NULL)
SELECT * FROM ranked WHERE rnk <= 2 ORDER BY department_name, rnk;

-- 5. 2nd highest
WITH r AS (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) rnk
           FROM employees WHERE salary IS NOT NULL)
SELECT DISTINCT salary FROM r WHERE rnk = 2;

-- 6. Running total
SELECT order_date, amount, SUM(amount) OVER (ORDER BY order_date, id) AS running_total
FROM orders ORDER BY order_date, id;

-- 8. Har row ke saath company average
SELECT name, salary, ROUND(AVG(salary) OVER ()) AS company_avg,
  salary - ROUND(AVG(salary) OVER ()) AS diff
FROM employees WHERE salary IS NOT NULL ORDER BY salary DESC;

-- 9. Quartiles
SELECT name, salary, NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees WHERE salary IS NOT NULL;

-- 10. Customer running total
SELECT c.name, o.order_date, o.amount,
  SUM(o.amount) OVER (PARTITION BY c.id ORDER BY o.order_date, o.id) AS running
FROM orders o JOIN customers c ON o.customer_id = c.id ORDER BY c.name, o.order_date;

-- 11. Top earner per department (FIRST_VALUE)
SELECT DISTINCT d.department_name,
  FIRST_VALUE(e.name) OVER (PARTITION BY e.department_id ORDER BY e.salary DESC) AS top_earner
FROM employees e JOIN departments d ON e.department_id = d.id WHERE e.salary IS NOT NULL;

-- 12. Percentile
SELECT name, salary, ROUND(PERCENT_RANK() OVER (ORDER BY salary) * 100, 1) AS percentile
FROM employees WHERE salary IS NOT NULL ORDER BY salary DESC;


-- ================================================================
-- STEP 17 — TRANSACTIONS
-- ================================================================

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER CHECK (balance >= 0));
INSERT INTO accounts VALUES (1,'Noman',10000), (2,'Ali',5000);

-- 1. Transfer transaction
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 2000 WHERE id = 1;
UPDATE accounts SET balance = balance + 2000 WHERE id = 2;
COMMIT;
SELECT * FROM accounts;

-- 2. Rollback
BEGIN TRANSACTION;
UPDATE accounts SET balance = 0 WHERE id = 1;
ROLLBACK;
SELECT * FROM accounts;

-- 3. Savepoint
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance + 500 WHERE id = 1;
SAVEPOINT sp1;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
ROLLBACK TO sp1;
COMMIT;
SELECT * FROM accounts;

DROP TABLE accounts;
