# 🏆 Employee Management System (EMS)

**Python + SQL ka capstone project.** Phase 1–3 me jo seekha, sab yahan use hua hai.

---

## Chalao

```bash
cd MASTERY/phase4_python_db/ems

python3 main.py        # app
python3 test_ems.py    # tests (71 tests)
python3 database.py    # connection flow demo
```

Koi setup nahi chahiye — SQLite pe chalta hai, database khud ban jaata hai.

---

## Features

| # | Feature | SQL Concepts |
|---|---|---|
| 1 | Add employee | `INSERT` + validation |
| 2 | View employees | `SELECT` + `LEFT JOIN` + `LIMIT` |
| 3 | Search employee | `LIKE` + parameterized query |
| 4 | Update employee | `UPDATE` + dynamic query + whitelist |
| 5 | Delete (soft + hard) | `DELETE` / `UPDATE status` |
| 6 | Search by department | `JOIN` + `GROUP BY` |
| 7 | Salary filtering | `BETWEEN` + `CASE` (bands) |
| 8 | Statistics dashboard | `COUNT` `AVG` `SUM` `MAX` + subquery |
| 9 | Export to CSV | Python `csv` module |

---

## File Structure

```
ems/
├── config.py       # settings — DB_TYPE yahan badlo
├── database.py     # connection, cursor, query helpers
├── models.py       # business logic + CRUD + validation
├── main.py         # menu UI
├── test_ems.py     # 71 automated tests
└── README.md
```

**Ye 3-layer architecture hai:**
```
main.py      (UI)        <- user se baat
   ↓
models.py    (Logic)     <- validation + business rules
   ↓
database.py  (Data)      <- connection + queries
   ↓
SQLite / MySQL
```

Django me bhi exactly yahi hota hai: `views.py` → `models.py` → database. **Isliye ye project Django ki seedhi tayyari hai.**

---

## Connection Flow (Interview Me Ye Bolna)

```
Python
  ↓
sqlite3 / mysql.connector
  ↓
CONNECTION      conn = sqlite3.connect("ems.db")
  ↓
CURSOR          cursor = conn.cursor()
  ↓
SQL QUERY       cursor.execute("SELECT ... WHERE id = ?", (1,))
  ↓
RESULT          cursor.fetchall()   /   fetchone()
  ↓
COMMIT          conn.commit()       (write operations pe)
  ↓
CLOSE           cursor.close(); conn.close()
```

Live demo: `python3 database.py`

---

## MySQL Pe Switch Karna

1. MySQL install karo
2. `pip install mysql-connector-python`
3. Database banao:
   ```sql
   CREATE DATABASE ems_db;
   ```
4. `config.py` me:
   ```python
   DB_TYPE = "mysql"
   MYSQL_CONFIG = {..., "password": "tera_password", ...}
   ```
5. `python3 main.py` — bas, ho gaya

**Poora app bina kisi aur change ke MySQL pe chalega.** `config.q()` function automatically `?` ko `%s` me badal deta hai.

---

## Security — Isme Kya Kya Hai

### 1. Parameterized Queries (har jagah)
```python
# ❌ KABHI NAHI
cursor.execute(f"SELECT * FROM employees WHERE name = '{name}'")

# ✅ HAMESHA
cursor.execute("SELECT * FROM employees WHERE name = ?", (name,))
```

### 2. Column Whitelist (dynamic UPDATE me)
```python
allowed = {"name": ..., "email": ..., "salary": ...}
if key not in allowed:
    raise ValidationError(...)     # user column name inject nahi kar sakta
```

### 3. Input Validation (regex se)
Email, phone, salary, date — sab validate hote hain **database me jaane se pehle**.

### 4. Transactions
```python
try:
    yield cursor
    conn.commit()
except Exception:
    conn.rollback()      # error pe sab cancel
    raise
finally:
    cursor.close()
    conn.close()
```

**Test:** app me search karke `' OR '1'='1` ya `'; DROP TABLE employees; --` daalo. Kuch nahi hoga.

---

## Tests

```bash
python3 test_ems.py
```

71 tests — CRUD, validation, filters, reports, **SQL injection attacks**.

Testing seekhna important hai — job me expect kiya jaata hai.

---

## 🎯 Tera Asli Task

Is code ko **padh lena kaafi nahi hai**.

1. ✅ Chalao, har feature try karo
2. ✅ Code padho, samjho
3. 🏆 **Band karo aur ZERO se khud likho** — dekh ke nahi, soch ke
4. 🏆 2 naye features khud add karo:
   - Attendance tracking
   - Leave management
   - Salary slip generator
   - Department-wise report export
   - Employee photo upload

Jab tu ye **bina dekhe** likh sake, tera foundation pakka hai. **Tab Django start kar.**

---

## Resume Pe Kaise Likhein

> **Employee Management System** — Python, SQLite/MySQL
> CLI-based CRUD application with layered architecture (UI / business logic / data access).
> Implemented parameterized queries and input validation to prevent SQL injection,
> transaction handling with automatic rollback, soft-delete pattern, and aggregate
> reporting (department statistics, salary bands, city distribution).
> 71 automated tests covering CRUD operations, validation rules, and injection attacks.
> *GitHub: [link]*
