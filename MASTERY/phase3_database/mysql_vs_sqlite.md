# MySQL vs SQLite — Cheatsheet

Practice SQLite pe kiya (zero setup). Job me MySQL milega. **95% same hai** — ye rahe fark.

---

## 1. Data Types

| Concept | MySQL | SQLite |
|---|---|---|
| Integer | `INT`, `BIGINT`, `TINYINT` | `INTEGER` |
| Auto increment | `INT AUTO_INCREMENT` | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| String (short) | `VARCHAR(100)` | `TEXT` |
| String (long) | `TEXT`, `LONGTEXT` | `TEXT` |
| Decimal/Money | `DECIMAL(10,2)` | `REAL` / `NUMERIC` |
| Boolean | `BOOLEAN` / `TINYINT(1)` | `INTEGER` (0/1) |
| Date | `DATE`, `DATETIME`, `TIMESTAMP` | `TEXT` ya `INTEGER` |
| Enum | `ENUM('a','b')` | ❌ nahi — `CHECK` use karo |

> SQLite me **dynamic typing** hai — column type ek suggestion hai, strict nahi. MySQL strict hai.

---

## 2. Auto Increment

```sql
-- MySQL
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- SQLite
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);
-- Ya simply: id INTEGER PRIMARY KEY  (automatically autoincrement hota hai)
```

---

## 3. String Functions

| Kaam | MySQL | SQLite |
|---|---|---|
| Jodna | `CONCAT(a, b)` | `a \|\| b` |
| Substring | `SUBSTRING(s,1,7)` | `SUBSTR(s,1,7)` |
| Group concat | `GROUP_CONCAT(x SEPARATOR ', ')` | `GROUP_CONCAT(x, ', ')` |
| Length | `LENGTH(s)` / `CHAR_LENGTH(s)` | `LENGTH(s)` |
| Upper/Lower | `UPPER()` / `LOWER()` | same |

---

## 4. Date Functions

| Kaam | MySQL | SQLite |
|---|---|---|
| Aaj | `CURDATE()`, `NOW()` | `date('now')`, `datetime('now')` |
| Add days | `DATE_ADD(d, INTERVAL 1 DAY)` | `date(d, '+1 day')` |
| Format | `DATE_FORMAT(d, '%Y-%m')` | `strftime('%Y-%m', d)` |
| Year nikalo | `YEAR(d)` | `strftime('%Y', d)` |
| Difference | `DATEDIFF(a, b)` | `julianday(a) - julianday(b)` |

---

## 5. NULL Handling

| MySQL | SQLite |
|---|---|
| `IFNULL(x, 0)` | `IFNULL(x, 0)` ✅ same |
| `COALESCE(x, 0)` | `COALESCE(x, 0)` ✅ same |
| `IF(cond, a, b)` | `IIF(cond, a, b)` |

---

## 6. Jo SQLite Me NAHI Hai

| Feature | Workaround |
|---|---|
| `RIGHT JOIN` (3.39 se pehle) | Tables swap karke `LEFT JOIN` |
| `FULL OUTER JOIN` | `LEFT JOIN UNION RIGHT JOIN` |
| `ANY` / `ALL` | `> (SELECT MIN(...))` / `> (SELECT MAX(...))` |
| Stored Procedures | Python code me logic likho |
| Users / Permissions | File-level permissions |
| `SHOW TABLES` | `.tables` ya `SELECT name FROM sqlite_master WHERE type='table'` |
| `DESCRIBE table` | `.schema table` ya `PRAGMA table_info(table)` |

> **Note:** MySQL me `FULL OUTER JOIN` bhi nahi hai! Wahan bhi UNION use karte hain.

---

## 7. Meta Commands

| Kaam | MySQL | SQLite |
|---|---|---|
| Databases list | `SHOW DATABASES;` | (file = database) |
| Tables list | `SHOW TABLES;` | `.tables` |
| Table structure | `DESCRIBE employees;` | `.schema employees` / `PRAGMA table_info(employees)` |
| Indexes | `SHOW INDEX FROM employees;` | `PRAGMA index_list(employees)` |
| Query plan | `EXPLAIN SELECT ...` | `EXPLAIN QUERY PLAN SELECT ...` |

---

## 8. Python Connection

```python
# ---------- SQLite ----------
import sqlite3
conn = sqlite3.connect("company.db")
cur = conn.cursor()
cur.execute("SELECT * FROM employees WHERE id = ?", (1,))     # ? placeholder
rows = cur.fetchall()
conn.commit()
conn.close()

# ---------- MySQL ----------
import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="company"
)
cur = conn.cursor()
cur.execute("SELECT * FROM employees WHERE id = %s", (1,))    # %s placeholder
rows = cur.fetchall()
conn.commit()
conn.close()
```

**Sabse bada fark:** placeholder — SQLite `?`, MySQL `%s`.
Baaki `connection → cursor → execute → fetch → close` flow **bilkul same**.

---

## 9. LIMIT / OFFSET

Dono me same:
```sql
SELECT * FROM employees ORDER BY salary DESC LIMIT 5 OFFSET 10;
SELECT * FROM employees LIMIT 10, 5;   -- MySQL ka short form (offset, count)
```

---

## 10. Transactions

| MySQL | SQLite |
|---|---|
| `START TRANSACTION;` | `BEGIN TRANSACTION;` |
| `BEGIN;` ✅ | `BEGIN;` ✅ |
| `COMMIT;` | `COMMIT;` |
| `ROLLBACK;` | `ROLLBACK;` |
| `SAVEPOINT x;` | `SAVEPOINT x;` |

> Python me SQLite default autocommit karta hai. Manual control ke liye:
> `sqlite3.connect(db, isolation_level=None)`

---

## Bottom Line

Tera SQL knowledge **transfer ho jaayega**. Sirf ye 5 cheezein yaad rakh:

1. `AUTO_INCREMENT` (MySQL) vs `AUTOINCREMENT` (SQLite)
2. `CONCAT()` vs `||`
3. `DATE_FORMAT()` vs `strftime()`
4. Placeholder: `%s` vs `?`
5. `VARCHAR(n)` vs `TEXT`
