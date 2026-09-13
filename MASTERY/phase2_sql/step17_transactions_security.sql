-- ================================================================
-- STEP 17 — TRANSACTIONS + SECURITY  🔴🔴
-- COMMIT, ROLLBACK, SAVEPOINT, SQL Injection, Parameterized Queries
-- ================================================================
-- Chalao:  python3 phase2_sql/run_sql.py phase2_sql/step17_transactions_security.sql
--
-- NOTE: Transaction ka LIVE demo Python me hai:
--       python3 phase2_sql/transactions_demo.py
--       Wahan rollback actually hota hua dikhega.
-- ================================================================


-- ================================================================
-- 1. TRANSACTION KYA HAI?
-- ================================================================
-- Ek ya zyada SQL statements ka group jo SAATH me chalte hain.
-- Ya to SAB successful, ya SAB cancel. Beech me kuch nahi.
--
-- CLASSIC EXAMPLE — Bank transfer:
--   Step 1: A ke account se 1000 kaato
--   Step 2: B ke account me 1000 daalo
--
-- Agar Step 1 ho gaya aur Step 2 fail ho gaya?
-- Paisa GAYAB! Isliye transaction chahiye.


-- ================================================================
-- 2. ACID PROPERTIES (INTERVIEW ME 100% POOCHHTE HAIN)
-- ================================================================
-- A - ATOMICITY   : Sab ya kuch nahi. Beech me nahi ruk sakta.
-- C - CONSISTENCY : DB ek valid state se doosri valid state me jaaye.
--                   Constraints kabhi toot nahi sakte.
-- I - ISOLATION   : Ek transaction doosre ko disturb nahi karega.
-- D - DURABILITY  : COMMIT ke baad data pakka. Power fail ho to bhi rahega.


-- ================================================================
-- 3. COMMIT — changes pakke karo
-- ================================================================

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
    id      INTEGER PRIMARY KEY,
    owner   TEXT NOT NULL,
    balance INTEGER NOT NULL CHECK (balance >= 0)
);

INSERT INTO accounts VALUES (1, 'Noman', 10000), (2, 'Ali', 5000);

SELECT * FROM accounts;

-- SUCCESSFUL TRANSFER: Noman se Ali ko 2000
BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 2000 WHERE id = 1;
UPDATE accounts SET balance = balance + 2000 WHERE id = 2;

COMMIT;

SELECT * FROM accounts;
-- ^^ Noman: 8000, Ali: 7000. COMMIT ke baad ye PAKKA hai.


-- ================================================================
-- 4. ROLLBACK — changes cancel karo
-- ================================================================

BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 5000 WHERE id = 1;
UPDATE accounts SET balance = balance + 5000 WHERE id = 2;

-- Socho yahan kuch galat pata chala (fraud detect hua)
ROLLBACK;

SELECT * FROM accounts;
-- ^^ Balance WAPAS purana. Kuch nahi badla. Ye ROLLBACK ki power hai.


-- ================================================================
-- 5. SAVEPOINT — partial rollback
-- ================================================================

BEGIN TRANSACTION;

UPDATE accounts SET balance = balance + 1000 WHERE id = 1;
SAVEPOINT after_bonus;

UPDATE accounts SET balance = balance - 500 WHERE id = 1;
UPDATE accounts SET balance = balance - 500 WHERE id = 2;

-- Sirf savepoint ke BAAD wala cancel karo
ROLLBACK TO after_bonus;

COMMIT;

SELECT * FROM accounts;
-- ^^ Bonus (+1000) bacha, deductions cancel ho gaye


-- ================================================================
-- 6. CONSTRAINT VIOLATION -> automatic rollback
-- ================================================================
-- accounts table me CHECK (balance >= 0) hai

SELECT * FROM accounts;

-- ⬇️ AGLI LINE JAAN BUJH KE FAIL HOGI — ye CHECK constraint ka DEMO hai.
--    "CHECK constraint failed" wala message dikhega = SAHI hai, ghabrana nahi.
--    Balance negative ho raha tha, DB ne khud rok diya.
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 999999 WHERE id = 1;
ROLLBACK;

SELECT * FROM accounts;
-- ^^ Kuch nahi badla


-- ================================================================
-- 7. SQL INJECTION — SABSE BADA SECURITY THREAT 🔴🔴🔴
-- ================================================================
--
-- ❌ GALAT CODE (Python) — string concatenation:
--
--   user_input = input("Username: ")
--   query = "SELECT * FROM users WHERE username = '" + user_input + "'"
--   cursor.execute(query)
--
-- ATTACKER kya likhega?
--
--   Input:  admin' --
--   Query:  SELECT * FROM users WHERE username = 'admin' --'
--           ^^ -- ke baad sab comment ho gaya, password check UD GAYA
--
--   Input:  ' OR '1'='1
--   Query:  SELECT * FROM users WHERE username = '' OR '1'='1'
--           ^^ '1'='1' hamesha TRUE -> SAARE users mil gaye
--
--   Input:  '; DROP TABLE users; --
--   Query:  SELECT * FROM users WHERE username = ''; DROP TABLE users; --'
--           ^^ POORI TABLE DELETE 💀
--
--
-- ✅ SAHI CODE — PARAMETERIZED QUERY (placeholder use karo):
--
--   # SQLite
--   cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,))
--
--   # MySQL (mysql-connector)
--   cursor.execute("SELECT * FROM users WHERE username = %s", (user_input,))
--
--   # PostgreSQL (psycopg2)
--   cursor.execute("SELECT * FROM users WHERE username = %s", (user_input,))
--
--
-- YE KYUN KAAM KARTA HAI?
--   Database query ka STRUCTURE pehle compile karta hai,
--   phir user ka input sirf DATA ki tarah bhejta hai.
--   Input kabhi SQL code nahi ban sakta. Bas.
--
--
-- ⚠️ PLACEHOLDER ke saath TUPLE bhejna zaroori hai:
--   cursor.execute("... = ?", (value,))     ✅ tuple (comma dhyan se!)
--   cursor.execute("... = ?", value)        ❌ error
--
--
-- ⚠️ TABLE/COLUMN NAME placeholder se NAHI aata:
--   cursor.execute("SELECT * FROM ?", (table,))     ❌ kaam nahi karega
--   Solution: whitelist banao
--     ALLOWED = {"employees", "departments"}
--     if table not in ALLOWED: raise ValueError("Invalid table")
--     cursor.execute(f"SELECT * FROM {table}")
--
--
-- BACHNE KE AUR TAREEKE:
--   1. Parameterized queries (sabse zaroori)
--   2. ORM use karo (Django ORM automatically safe hai)
--   3. Input validation
--   4. Least privilege — app user ko DROP permission mat do
--   5. Stored procedures
--   6. Error messages me SQL detail mat dikhao


-- ================================================================
-- 8. USER PERMISSIONS (DCL) — MySQL syntax
-- ================================================================
-- SQLite me users nahi hote, ye MySQL me chalega:
--
--   CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
--
--   -- Sirf zaroori permission do (LEAST PRIVILEGE)
--   GRANT SELECT, INSERT, UPDATE ON company.* TO 'app_user'@'localhost';
--
--   -- DROP/DELETE ki permission MAT do production app ko
--
--   REVOKE INSERT ON company.* FROM 'app_user'@'localhost';
--   FLUSH PRIVILEGES;
--   SHOW GRANTS FOR 'app_user'@'localhost';


-- ================================================================
-- 9. ISOLATION LEVELS (advanced, par poochh lete hain)
-- ================================================================
-- READ UNCOMMITTED -> dirty reads allowed (sabse fast, sabse risky)
-- READ COMMITTED   -> sirf committed data dikhega
-- REPEATABLE READ  -> same query same result (MySQL InnoDB default)
-- SERIALIZABLE     -> poora isolation (sabse safe, sabse slow)
--
-- PROBLEMS jo isolation rokta hai:
--   Dirty Read       -> uncommitted data padh liya
--   Non-repeatable   -> same query, alag result (beech me koi UPDATE kar gaya)
--   Phantom Read     -> nayi rows aa gayi beech me
--
-- MySQL me:  SET TRANSACTION ISOLATION LEVEL READ COMMITTED;


-- ================================================================
-- 10. CLEANUP
-- ================================================================

DROP TABLE IF EXISTS accounts;


-- ================================================================
-- INTERVIEW QUESTIONS
-- ================================================================
-- Q1. Transaction kya hai?
--     SQL statements ka group jo ek unit ki tarah chalta hai.
--     Ya sab commit, ya sab rollback.
--
-- Q2. ACID kya hai?
--     Atomicity, Consistency, Isolation, Durability
--
-- Q3. COMMIT vs ROLLBACK?
--     COMMIT   -> changes permanent
--     ROLLBACK -> changes cancel, purani state
--
-- Q4. SAVEPOINT kya hai?
--     Transaction ke beech ka marker. Wahan tak rollback kar sakte ho
--     bina poora transaction cancel kiye.
--
-- Q5. SQL Injection kya hai? (MOST IMPORTANT SECURITY Q)
--     Attacker user input ke through SQL code inject karta hai.
--     Data chura sakta hai, delete kar sakta hai, login bypass kar sakta hai.
--
-- Q6. SQL Injection se kaise bachein?
--     PARAMETERIZED QUERIES use karo (? ya %s placeholder).
--     Kabhi string concatenation se query mat banao.
--     ORM use karo (Django ORM safe hai by default).
--
-- Q7. Parameterized query kaam kaise karti hai?
--     Query structure pehle compile hoti hai, input baad me
--     sirf DATA ki tarah bind hota hai. Input kabhi code nahi ban sakta.
--
-- Q8. DELETE vs TRUNCATE — rollback ho sakta hai?
--     DELETE   -> DML, transaction me rollback HO SAKTA hai
--     TRUNCATE -> DDL, auto-commit, rollback NAHI hota
--
-- Q9. Deadlock kya hai?
--     Do transactions ek doosre ka lock wait kar rahe hain, dono atke.
--     DB ek ko kill kar deta hai. Bachne ke liye: same order me lock lo,
--     transactions chhote rakho.
--
-- Q10. Isolation levels?
--      READ UNCOMMITTED < READ COMMITTED < REPEATABLE READ < SERIALIZABLE


-- ================================================================
-- PRACTICE
-- ================================================================
-- 1.  accounts table banao aur transfer transaction likho
-- 2.  Transaction me ROLLBACK karke dekho ki data wapas aata hai
-- 3.  SAVEPOINT use karke partial rollback karo
-- 4.  CHECK constraint lagao aur usko todne ki koshish karo
-- 5.  Python me transaction likho (transactions_demo.py dekho)
-- 6.  Ek SQL injection vulnerable code likho, phir usko fix karo
-- 7.  Parameterized query ke saath search function banao
-- 8.  Ek function jo table name whitelist se validate kare
