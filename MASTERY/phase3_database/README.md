# 🗄️ PHASE 3 — DATABASE (MySQL First)

**SQL = language.** **Database = system jo wo language samajhta hai.**

Abhi teen database ek saath mat padhna. **MySQL pehle.** Baaki baad me.

---

## Order

| Kab | Kya | Kyun |
|---|---|---|
| **Abhi** 🔴🔴 | **MySQL** | India me sabse zyada job posts, tere notes bhi MySQL ke hain |
| Baad me 🟡 | PostgreSQL | Django production me yahi chalta hai |
| Kabhi 🟢 | MongoDB | NoSQL, alag concept, abhi zarurat nahi |

---

## 1. MySQL Install

1. [dev.mysql.com/downloads/installer](https://dev.mysql.com/downloads/installer/) se **MySQL Installer for Windows** download karo
2. Setup Type: **Developer Default** chuno
3. Root password set karo — **likh ke rakho, bhoolna mat**
4. **MySQL Workbench** bhi install hoga — usse GUI me kaam karna aasan hai

**Check karo:**
```bash
mysql --version
mysql -u root -p
```

**Pehla command:**
```sql
SHOW DATABASES;
CREATE DATABASE company;
USE company;
SHOW TABLES;
```

---

## 2. Core Concepts

### Database → Table → Row → Column

```
DATABASE: company
   │
   ├── TABLE: employees
   │      ├── COLUMNS: id, name, salary, department_id
   │      └── ROWS:    (1, 'Noman', 30000, 1)
   │                   (2, 'Ali', 45000, 2)
   │
   └── TABLE: departments
```

| Term | Matlab |
|---|---|
| **Database** | Poora data ka container |
| **Table** | Ek entity ka data (employees, orders) |
| **Row / Record / Tuple** | Ek entry (ek employee) |
| **Column / Field / Attribute** | Ek property (name, salary) |

---

## 3. KEYS 🔴🔴 (Interview me pakka)

### Primary Key
Har row ki **unique pehchaan**. Ek table me sirf **ek** PK.
- UNIQUE + NOT NULL automatically
- Index automatically banta hai

```sql
id INT PRIMARY KEY AUTO_INCREMENT
```

### Foreign Key
Doosri table ke Primary Key ko point karta hai. **Relationship** banata hai.

```sql
department_id INT,
FOREIGN KEY (department_id) REFERENCES departments(id)
```

**ON DELETE options:**
| Option | Kya hoga jab parent delete ho |
|---|---|
| `CASCADE` | Child rows bhi delete |
| `SET NULL` | Child ka FK NULL ho jaayega |
| `RESTRICT` | Delete hi nahi hone dega (default) |
| `NO ACTION` | RESTRICT jaisa |

### Baaki Keys

| Key | Matlab |
|---|---|
| **Candidate Key** | Jo PK ban sakti thi (id, email dono unique hain) |
| **Alternate Key** | Candidate key jo PK nahi bani (email) |
| **Composite Key** | 2+ columns milke PK (student_id + course_id) |
| **Super Key** | Koi bhi column set jo unique ho |
| **Unique Key** | Unique values, par NULL allow (PK me NULL nahi) |

**PK vs Unique Key** (classic question):
| | Primary Key | Unique Key |
|---|---|---|
| NULL | Nahi | Haan (ek NULL) |
| Kitne | Ek table me 1 | Kitne bhi |
| Index | Clustered | Non-clustered |

---

## 4. CONSTRAINTS

```sql
CREATE TABLE employees (
    id       INT PRIMARY KEY AUTO_INCREMENT,     -- unique + not null
    name     VARCHAR(100) NOT NULL,              -- khaali nahi
    email    VARCHAR(100) UNIQUE,                -- duplicate nahi
    salary   DECIMAL(10,2) CHECK (salary > 0),   -- condition
    status   VARCHAR(20) DEFAULT 'Active',       -- default value
    dept_id  INT,
    FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE SET NULL
);
```

---

## 5. RELATIONSHIPS 🔴

### One-to-One (1:1)
Ek employee ka ek passport.
```sql
CREATE TABLE passports (
    id INT PRIMARY KEY,
    employee_id INT UNIQUE,        -- UNIQUE se 1:1 banta hai
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
```

### One-to-Many (1:N) — sabse common
Ek department me kai employees.
```sql
-- FK "many" wali side pe jaata hai
CREATE TABLE employees (
    id INT PRIMARY KEY,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

### Many-to-Many (M:N)
Ek employee kai projects me, ek project me kai employees.
**Junction table chahiye:**
```sql
CREATE TABLE assignments (
    employee_id INT,
    project_id  INT,
    hours INT,
    PRIMARY KEY (employee_id, project_id),      -- composite key
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (project_id)  REFERENCES projects(id)
);
```

---

## 6. NORMALIZATION 🔴

**Kyun?** Data duplication hatao, anomalies rokо.

### Unnormalized (kharab)
| id | name | dept | dept_location | skills |
|---|---|---|---|---|
| 1 | Noman | IT | Hyderabad | Python, SQL |
| 2 | Sara | IT | Hyderabad | Django |

Problems:
- "Hyderabad" baar baar repeat (waste)
- IT ki location badli to **har row** update karni padegi (update anomaly)
- Saare IT employees delete kiye to IT department ka data hi gayab (delete anomaly)

### 1NF — Atomic Values
Har cell me **ek** value. Repeating groups nahi.
```
❌ skills = "Python, SQL"
✅ alag skills table
```

### 2NF — 1NF + No Partial Dependency
Har non-key column **poori** primary key pe depend kare (composite key me matter karta hai).

### 3NF — 2NF + No Transitive Dependency
Non-key column doosre non-key column pe depend na kare.
```
❌ employees(id, name, dept_id, dept_location)
   dept_location, dept_id pe depend karta hai — id pe nahi
✅ departments table alag banao
```

### BCNF
3NF ka stricter version. Har determinant super key hona chahiye.

**Interview short answer:**
> 1NF = atomic values
> 2NF = 1NF + no partial dependency
> 3NF = 2NF + no transitive dependency
> Practical me **3NF tak** kaafi hai.

### Denormalization
Jaan bujh ke duplicate rakhna **performance** ke liye (JOIN kam karne ke liye). Reporting/analytics me karte hain.

---

## 7. INDEXES 🔴

**Kya hai?** Book ka index jaisa — data dhoondhne ko fast banata hai.

```sql
CREATE INDEX idx_salary ON employees(salary);
CREATE INDEX idx_name_city ON employees(name, city);   -- composite
CREATE UNIQUE INDEX idx_email ON employees(email);
DROP INDEX idx_salary ON employees;
SHOW INDEX FROM employees;
EXPLAIN SELECT * FROM employees WHERE salary > 50000;  -- index use hua?
```

**Kab lagao:**
- ✅ WHERE me baar baar use hone wale columns
- ✅ JOIN ke columns (FK)
- ✅ ORDER BY ke columns

**Kab NAHI:**
- ❌ Chhoti tables
- ❌ Jo columns bahut baar UPDATE hote hain
- ❌ Low cardinality (jaise gender — sirf 2 values)

**Trade-off:** SELECT fast, par INSERT/UPDATE/DELETE slow (index bhi update karna padta hai) + extra disk space.

---

## 8. DATA TYPES (MySQL)

| Category | Types | Kab |
|---|---|---|
| Integer | `TINYINT`, `INT`, `BIGINT` | id, count, age |
| Decimal | `DECIMAL(10,2)` | **paisa** (FLOAT kabhi nahi!) |
| Float | `FLOAT`, `DOUBLE` | scientific calc |
| String | `CHAR(n)`, `VARCHAR(n)`, `TEXT` | naam, description |
| Date | `DATE`, `DATETIME`, `TIMESTAMP` | dates |
| Other | `BOOLEAN`, `ENUM`, `JSON`, `BLOB` | flags, options |

**CHAR vs VARCHAR:**
- `CHAR(10)` — fixed 10 bytes hamesha. Fixed length data ke liye (state code)
- `VARCHAR(10)` — jitna data utni jagah. Zyadatar yahi use karo

**⚠️ Paise ke liye hamesha `DECIMAL`, kabhi `FLOAT` nahi** — FLOAT me rounding errors aate hain.

---

## 9. ALTER TABLE

```sql
ALTER TABLE employees ADD COLUMN phone VARCHAR(15);
ALTER TABLE employees MODIFY COLUMN name VARCHAR(150);
ALTER TABLE employees CHANGE COLUMN phone mobile VARCHAR(15);
ALTER TABLE employees DROP COLUMN mobile;
ALTER TABLE employees ADD CONSTRAINT fk_dept
    FOREIGN KEY (department_id) REFERENCES departments(id);
ALTER TABLE employees RENAME TO staff;
```

---

## 10. Interview Questions

**Q1. DBMS vs RDBMS?**
DBMS — data store karta hai. RDBMS — tables me store karta hai + relationships + ACID. MySQL, PostgreSQL RDBMS hain.

**Q2. Primary Key vs Unique Key?**
PK — ek per table, NULL nahi. Unique — kitne bhi, ek NULL allow.

**Q3. Foreign Key kya karta hai?**
Do tables me relationship banata hai + referential integrity enforce karta hai (aisi value nahi daal sakte jo parent me na ho).

**Q4. Normalization kyun?**
Redundancy hatao, insert/update/delete anomalies roko, data consistent rakho.

**Q5. 1NF, 2NF, 3NF?**
1NF atomic, 2NF no partial dependency, 3NF no transitive dependency.

**Q6. Index kya hai? Fayda-nuksan?**
Fast lookup structure. SELECT fast, write slow, extra space.

**Q7. DELETE vs TRUNCATE vs DROP?**
DELETE — rows, WHERE chalta hai, rollback possible (DML)
TRUNCATE — saari rows, fast, rollback nahi (DDL)
DROP — table hi gayab (DDL)

**Q8. CHAR vs VARCHAR?**
CHAR fixed length, VARCHAR variable. VARCHAR zyadatar better.

**Q9. Paise ke liye kaunsa type?**
DECIMAL. FLOAT me precision errors aate hain.

**Q10. M:N relationship kaise banate hain?**
Junction/bridge table se, jisme dono ki FK ho.

---

## Files Is Folder Me

| File | Kya |
|---|---|
| `schema_mysql.sql` | Poora MySQL schema — MySQL pe seedha chala do |
| `mysql_vs_sqlite.md` | Syntax differences cheatsheet |

---

## Practice

1. MySQL install karke Workbench se connect karo
2. `company` database banao
3. `schema_mysql.sql` chalao
4. `departments` aur `employees` tables banao FK ke saath
5. FK todne ki koshish karo (invalid dept_id daalo) — error dekho
6. `ON DELETE CASCADE` test karo
7. M:N ke liye `assignments` table banao
8. Salary pe index lagao, `EXPLAIN` se check karo
9. Ek unnormalized table ko 3NF me todo
10. `ALTER TABLE` se column add/modify/drop karo
