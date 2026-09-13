-- ================================================================
-- STEP 10 — FILTERING  🔴🔴
-- WHERE, AND, OR, NOT, IN, BETWEEN, LIKE, IS NULL, IS NOT NULL
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step10_filtering.sql
-- ================================================================


-- ================================================================
-- 1. WHERE — basic condition
-- ================================================================
-- Tera example:
--   SELECT * FROM employees WHERE salary > 30000;

SELECT name, salary FROM employees
WHERE salary > 30000
ORDER BY salary DESC;

-- Comparison operators:  =  !=  <>  >  <  >=  <=
SELECT name, salary FROM employees WHERE salary = 45000;
SELECT name, city FROM employees WHERE city != 'Hyderabad' LIMIT 5;
SELECT name, salary FROM employees WHERE salary >= 60000;


-- ================================================================
-- 2. AND / OR / NOT
-- ================================================================

-- AND — DONO condition sach honi chahiye
SELECT name, salary, city FROM employees
WHERE salary > 40000 AND city = 'Hyderabad';

-- OR — koi EK sach ho
SELECT name, city FROM employees
WHERE city = 'Mumbai' OR city = 'Delhi'
LIMIT 6;

-- NOT — ulta
SELECT name, city FROM employees
WHERE NOT city = 'Hyderabad'
LIMIT 5;

-- ⚠️ AND ka priority OR se ZYADA hota hai — BRACKETS lagao
-- Bina brackets (galat result de sakta hai):
SELECT name, salary, city FROM employees
WHERE city = 'Mumbai' OR city = 'Delhi' AND salary > 60000;

-- Brackets ke saath (SAHI):
SELECT name, salary, city FROM employees
WHERE (city = 'Mumbai' OR city = 'Delhi') AND salary > 60000;

-- ^^ Dono ka result compare karo. Ye interview me poochhte hain.


-- ================================================================
-- 3. IN — multiple values (OR ka chhota version)
-- ================================================================

-- Ye lamba tareeka:
SELECT name, city FROM employees
WHERE city = 'Mumbai' OR city = 'Delhi' OR city = 'Pune';

-- Ye chhota aur saaf:
SELECT name, city FROM employees
WHERE city IN ('Mumbai', 'Delhi', 'Pune');

-- NOT IN
SELECT name, city FROM employees
WHERE city NOT IN ('Mumbai', 'Delhi');

-- IN with subquery (Step 14 me detail me)
SELECT name FROM employees
WHERE department_id IN (SELECT id FROM departments WHERE location = 'Mumbai');

-- ⚠️ NOT IN + NULL = KHATRA
-- Agar subquery me ek bhi NULL aa gaya to NOT IN kuch bhi return nahi karega.
-- Isliye NOT EXISTS ya IS NOT NULL lagao.


-- ================================================================
-- 4. BETWEEN — range (DONO ends INCLUSIVE hote hain)
-- ================================================================

SELECT name, salary FROM employees
WHERE salary BETWEEN 40000 AND 60000
ORDER BY salary;

-- Ye bilkul same hai:
SELECT name, salary FROM employees
WHERE salary >= 40000 AND salary <= 60000
ORDER BY salary;

-- NOT BETWEEN
SELECT name, salary FROM employees
WHERE salary NOT BETWEEN 40000 AND 60000 AND salary IS NOT NULL;

-- Dates pe bhi kaam karta hai
SELECT name, hire_date FROM employees
WHERE hire_date BETWEEN '2022-01-01' AND '2023-12-31'
ORDER BY hire_date;


-- ================================================================
-- 5. LIKE — pattern matching
-- ================================================================
-- WILDCARDS:
--   %  = kitne bhi characters (0 ya zyada)
--   _  = exactly EK character

-- 'A' se shuru hone wale
SELECT name FROM employees WHERE name LIKE 'A%';

-- 'a' pe khatam hone wale
SELECT name FROM employees WHERE name LIKE '%a';

-- Beech me 'Kumar' ho
SELECT name FROM employees WHERE name LIKE '%Kumar%';

-- 5 characters ka naam (5 underscores)
SELECT name FROM employees WHERE name LIKE '_____';

-- Doosra character 'r' ho
SELECT name FROM employees WHERE name LIKE '_r%';

-- Email pattern
SELECT name, email FROM employees
WHERE email LIKE '%@techcorp.com'
LIMIT 5;

-- NOT LIKE
SELECT name FROM employees
WHERE name NOT LIKE 'A%'
LIMIT 5;

-- ⚠️ LIKE '%something' (shuru me %) INDEX use nahi karta = SLOW on big tables


-- ================================================================
-- 6. IS NULL / IS NOT NULL  (BAHUT IMPORTANT)
-- ================================================================
-- ⚠️ NULL ke saath = ya != KABHI kaam nahi karta!
--    NULL = "pata nahi" hai, koi value nahi.
--    NULL = NULL  ->  ye bhi FALSE deta hai!

-- Ye GALAT hai (0 rows aayengi):
SELECT name FROM employees WHERE salary = NULL;

-- Ye SAHI hai:
SELECT id, name, salary FROM employees WHERE salary IS NULL;

-- IS NOT NULL
SELECT COUNT(*) AS salary_wale FROM employees WHERE salary IS NOT NULL;

-- Department assign nahi hua
SELECT id, name, department_id FROM employees WHERE department_id IS NULL;

-- Project jo khatam nahi hua
SELECT project_name, status, end_date FROM projects WHERE end_date IS NULL;

-- Customer jinka email nahi hai
SELECT name, email FROM customers WHERE email IS NULL;

-- COALESCE — NULL ki jagah default value
SELECT name,
       salary,
       COALESCE(salary, 0) AS salary_ya_zero,
       COALESCE(CAST(department_id AS TEXT), 'Not Assigned') AS dept
FROM employees
WHERE salary IS NULL OR department_id IS NULL;

-- IFNULL (SQLite/MySQL) — same kaam
SELECT name, IFNULL(salary, 0) AS salary FROM employees WHERE salary IS NULL;


-- ================================================================
-- 7. SAB MILA KE — real world query
-- ================================================================

SELECT name, salary, city, hire_date
FROM employees
WHERE salary IS NOT NULL
  AND salary BETWEEN 35000 AND 70000
  AND city IN ('Hyderabad', 'Mumbai', 'Delhi')
  AND name NOT LIKE 'R%'
ORDER BY salary DESC;


-- ================================================================
-- 8. ORDER BY — detail me
-- ================================================================

-- Ascending (default)
SELECT name, salary FROM employees WHERE salary IS NOT NULL ORDER BY salary LIMIT 5;

-- Descending
SELECT name, salary FROM employees WHERE salary IS NOT NULL ORDER BY salary DESC LIMIT 5;

-- Multiple columns — pehle city, phir salary
SELECT name, city, salary FROM employees
WHERE salary IS NOT NULL
ORDER BY city ASC, salary DESC
LIMIT 10;

-- Column number se (readable nahi, par chalta hai)
SELECT name, salary FROM employees WHERE salary IS NOT NULL ORDER BY 2 DESC LIMIT 3;


-- ================================================================
-- INTERVIEW QUESTIONS
-- ================================================================
-- Q1. WHERE aur HAVING me fark?
--     WHERE  -> rows filter karta hai, GROUP BY se PEHLE
--     HAVING -> groups filter karta hai, GROUP BY ke BAAD
--
-- Q2. NULL ke saath = kyun nahi chalta?
--     NULL "unknown" hai. Unknown = Unknown ka jawab bhi unknown hai.
--     Isliye IS NULL / IS NOT NULL use karte hain.
--
-- Q3. IN vs EXISTS?
--     IN     -> chhoti list ke liye theek
--     EXISTS -> badi subquery ke liye fast, pehla match milte hi ruk jaata hai
--
-- Q4. BETWEEN inclusive hai ya exclusive?
--     INCLUSIVE — dono ends included hain.
--
-- Q5. LIKE '%abc' slow kyun hai?
--     Shuru me % ho to index use nahi hota, poori table scan hoti hai.
--
-- Q6. AND aur OR me priority?
--     AND pehle evaluate hota hai. Brackets se control karo.


-- ================================================================
-- PRACTICE
-- ================================================================
-- 1.  50000 se zyada salary wale employees
-- 2.  Hyderabad ya Bangalore ke employees (IN use karo)
-- 3.  Salary 40000-60000 ke beech (BETWEEN)
-- 4.  Naam 'S' se shuru hone wale
-- 5.  Email me 'techcorp' ho
-- 6.  Jinki salary NULL hai
-- 7.  Jinka department assign nahi hua
-- 8.  Mumbai ke employees jinki salary 50000 se zyada (AND)
-- 9.  Delhi ya Mumbai ke, par salary 60000+ (brackets dhyan se!)
-- 10. Jo 2023 me join hue (hire_date BETWEEN)
-- 11. 6 character ke naam wale (underscore use karo)
-- 12. Jo IT ya HR me nahi hain (NOT IN + subquery)
