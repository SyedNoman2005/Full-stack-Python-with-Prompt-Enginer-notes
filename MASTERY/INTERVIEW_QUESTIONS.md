# 🎯 INTERVIEW QUESTION BANK — Python + SQL + Database + Git

Interview se **ek raat pehle** ye file padhna. Sab jawab yahin hain.

**Rule:** Jawab **bol ke** practice karo, mann me padh ke nahi. Bolna alag skill hai.

---

# 🐍 PYTHON

## Basics

**Q. Python ki khasiyat kya hai?**
Interpreted, dynamically typed, object-oriented, huge standard library ("batteries included"), readable syntax, cross-platform.

**Q. List vs Tuple?**
| List | Tuple |
|---|---|
| Mutable | Immutable |
| `[]` | `()` |
| Slow | Fast |
| Dict key nahi ban sakti | Ban sakti hai |

**Q. List vs Set vs Dict?**
List — ordered, duplicates allowed, index se access
Set — unordered, unique only, fast lookup (O(1))
Dict — key-value pairs, fast lookup, ordered (Python 3.7+)

**Q. Mutable vs Immutable?**
Mutable: `list`, `dict`, `set`
Immutable: `int`, `float`, `str`, `tuple`, `frozenset`

**Q. `==` vs `is`?**
`==` value compare karta hai, `is` memory address (identity).

**Q. Shallow vs Deep copy?**
`b = a` — same object
`b = a.copy()` — shallow (top level naya, nested same)
`copy.deepcopy(a)` — poora naya

**Q. String reverse kaise?**
`s[::-1]`

**Q. List se duplicates kaise hataye?**
`list(set(my_list))` — order chahiye to `list(dict.fromkeys(my_list))`

**Q. List comprehension kya hai?**
Ek line me list banane ka concise tareeka: `[x**2 for x in range(5) if x % 2 == 0]`

**Q. `range()` vs `xrange()`?**
Python 3 me sirf `range()` hai, jo lazy/generator jaisa behave karta hai.

---

## Functions

**Q. `*args` vs `**kwargs`?**
`*args` — variable positional arguments → **tuple**
`**kwargs` — variable keyword arguments → **dict**

**Q. `return` vs `print`?**
`return` value wapas deta hai (aage use hoti hai). `print` sirf display karta hai, function `None` return karta hai.

**Q. Lambda kya hai?**
Ek line ka anonymous function. `sorted()`, `map()`, `filter()` me use hota hai.

**Q. Local vs Global variable?**
Local — function ke andar. Global — poore module me. Function ke andar global badalne ke liye `global` keyword.

**Q. LEGB rule?**
Local → Enclosing → Global → Built-in. Python isi order me variable dhoondhta hai.

**Q. Mutable default argument ka trap?**
```python
def f(items=[]):     # ❌ SAB calls me SAME list share hoti hai
def f(items=None):   # ✅
    if items is None: items = []
```

**Q. Decorator kya hai?**
Function jo doosre function ko wrap karke uska behaviour badalta hai, bina code change kiye.
```python
@login_required
def my_view(request): ...
```

**Q. Generator kya hai?**
`yield` use karne wala function. Values ek-ek karke deta hai, poori list memory me nahi rakhta. Badi data ke liye memory efficient.

**Q. `yield` vs `return`?**
`return` — function khatam. `yield` — value deta hai par state bachaata hai, agli call se wahin se chalu.

---

## OOP 🔴 (Sabse Zyada Poochhte Hain)

**Q. OOP ke 4 pillars?**
1. **Encapsulation** — data + methods ek jagah, private data chhupao
2. **Inheritance** — parent ka code child me reuse
3. **Polymorphism** — ek naam, alag behaviour
4. **Abstraction** — kya karta hai dikhao, kaise karta hai chhupao

**Q. Class vs Object?**
Class = blueprint. Object = actual instance.

**Q. `self` kya hai?**
Current object ka reference. `obj.method()` ko Python `Class.method(obj)` banata hai.

**Q. `__init__` kya hai?**
Constructor — object banate hi automatically chalta hai, instance variables initialize karta hai.

**Q. `super()` kya karta hai?**
Parent class ka method call karta hai. Zyadatar `super().__init__()` ke liye.

**Q. Method Overriding vs Overloading?**
Overriding — child parent ka method dobara likhe. **Python me hota hai.**
Overloading — same naam, alag parameters. **Python me nahi hota** (default args / `*args` se kaam chalate hain).

**Q. Public / Protected / Private?**
`name` — public
`_name` — protected (convention)
`__name` — private (name mangling: `_ClassName__name`)
Python me sach me kuch private nahi — sab convention hai.

**Q. Abstract class kya hai?**
`ABC` se inherit karti hai, `@abstractmethod` hote hain. Object nahi ban sakta. Child ko abstract methods implement karna hi padta hai.

**Q. `@staticmethod` vs `@classmethod` vs instance method?**
| | Pehla param | Kab |
|---|---|---|
| instance | `self` | object ka data chahiye |
| class | `cls` | class ka data / alternative constructor |
| static | koi nahi | bas utility function |

**Q. `__str__` vs `__repr__`?**
`__str__` — `print()` ke liye, user-friendly
`__repr__` — debugging ke liye, developer-friendly

**Q. Class variable vs Instance variable?**
Class variable — sab objects me shared. Instance variable — har object ka apna.

**Q. Multiple inheritance aur MRO?**
`class C(A, B)`. MRO = Method Resolution Order, C3 linearization. `C.__mro__` se dekho.

**Q. Duck typing kya hai?**
Python inheritance nahi dekhta, bas method hai ya nahi ye dekhta hai. "Agar duck jaisa chalta hai, to duck hai."

---

## Exception Handling

**Q. `try` / `except` / `else` / `finally`?**
`try` — risky code
`except` — error handle
`else` — koi error **na** aaye to chalega
`finally` — **hamesha** chalega (cleanup ke liye)

**Q. `raise` kya karta hai?**
Manually exception phenkta hai. Validation me use hota hai.

**Q. Custom exception kaise banate hain?**
```python
class MyError(Exception): pass
raise MyError("message")
```

**Q. `except:` vs `except Exception:`?**
`except:` — sab kuch pakadta hai (`KeyboardInterrupt`, `SystemExit` bhi). **Bura.**
`except Exception:` — sirf normal exceptions. **Behtar.**

**Q. Exception order kaise likhein?**
Specific pehle, generic baad me. Warna generic sab pakad lega.

**Q. Common exceptions?**
`ValueError`, `TypeError`, `KeyError`, `IndexError`, `AttributeError`, `ZeroDivisionError`, `FileNotFoundError`, `NameError`, `ImportError`

---

## Files + JSON

**Q. `with` statement kyun?**
Context manager — file automatically close hoti hai, error aaye tab bhi.

**Q. `json.load` vs `json.loads`?**
`load` — FILE se. `loads` — STRING se (`s` = string).

**Q. `json.dump` vs `json.dumps`?**
`dump` — FILE me likhta hai. `dumps` — STRING return karta hai.

**Q. `'w'` vs `'a'` mode?**
`'w'` purana data mita deta hai, `'a'` end me jodta hai.

**Q. Python `set` JSON me kyun nahi jaata?**
JSON me `set` type hi nahi hai. `list(my_set)` karo.

---

## Modules + venv

**Q. Module vs Package?**
Module — ek `.py` file. Package — folder with `__init__.py`.

**Q. `__name__ == "__main__"` kyun?**
Taaki file import hone pe test code na chale, sirf direct run pe chale.

**Q. Virtual environment kyun?**
Har project ki apni libraries, apne versions. Conflicts nahi hote.

**Q. `requirements.txt` kya hai?**
Dependencies ki list exact versions ke saath. `pip freeze > requirements.txt` se banti hai.

**Q. `pip list` vs `pip freeze`?**
`list` — readable table. `freeze` — `package==version` format.

---

# 🗄️ SQL

## Basics

**Q. DDL / DML / DCL / TCL?**
DDL — `CREATE`, `ALTER`, `DROP`, `TRUNCATE`
DML — `INSERT`, `UPDATE`, `DELETE`, `SELECT`
DCL — `GRANT`, `REVOKE`
TCL — `COMMIT`, `ROLLBACK`, `SAVEPOINT`

**Q. `DELETE` vs `TRUNCATE` vs `DROP`?**
| | DELETE | TRUNCATE | DROP |
|---|---|---|---|
| Kya hatata | rows | saari rows | poori table |
| `WHERE` | ✅ | ❌ | ❌ |
| Rollback | ✅ | ❌ | ❌ |
| Type | DML | DDL | DDL |

**Q. Query execution order?**
`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`

> Isliye `WHERE` me column alias nahi chalta, `ORDER BY` me chalta hai.

---

## Filtering

**Q. `WHERE` vs `HAVING`?**
`WHERE` — **rows** filter, `GROUP BY` se **pehle**, aggregate nahi chalta
`HAVING` — **groups** filter, `GROUP BY` ke **baad**, aggregate chalta hai

**Q. `NULL` ke saath `=` kyun nahi chalta?**
`NULL` "unknown" hai. Unknown = unknown ka jawab bhi unknown. `IS NULL` use karo.

**Q. `BETWEEN` inclusive hai?**
Haan, dono ends included.

**Q. `LIKE '%abc'` slow kyun?**
Shuru me `%` ho to index use nahi hota, full table scan.

**Q. `IN` vs `EXISTS`?**
`IN` — chhoti list, NULL ke saath problem
`EXISTS` — badi data me fast, NULL-safe, pehla match pe ruk jaata hai

**Q. `NOT IN` + NULL ka trap?**
Subquery me ek bhi NULL ho to `NOT IN` **kuch bhi** return nahi karta. `NOT EXISTS` use karo.

---

## Aggregates

**Q. `COUNT(*)` vs `COUNT(column)`?**
`COUNT(*)` — saari rows (NULL bhi)
`COUNT(column)` — sirf non-NULL values

**Q. `AVG` NULL ko kaise treat karta hai?**
Ignore karta hai. `SUM(salary)/COUNT(salary)`, NOT `/COUNT(*)`.

**Q. `GROUP BY` me `SELECT` ka rule?**
`SELECT` ka har column ya `GROUP BY` me ho ya aggregate ke andar.

---

## JOINs 🔥

**Q. JOIN types?**
| Type | Kya deta hai |
|---|---|
| `INNER` | Sirf matching rows dono taraf se |
| `LEFT` | Left ki saari + matching right (warna NULL) |
| `RIGHT` | Right ki saari + matching left |
| `FULL OUTER` | Dono ki saari (MySQL me nahi — `UNION` se) |
| `SELF` | Table khud se (employee-manager) |
| `CROSS` | Cartesian product (m × n) |

**Q. Jinke paas kuch nahi hai unhe kaise dhoondhein?**
**Anti-join pattern:**
```sql
SELECT c.* FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

**Q. LEFT JOIN me WHERE lagane se kya hota hai?**
Wo INNER JOIN ban jaata hai (NULL rows filter ho jaati hain). Condition `ON` clause me daalo.

**Q. JOIN vs Subquery — kaun fast?**
JOIN generally fast. Optimizer better handle karta hai. Correlated subquery sabse slow.

---

## CASE / Subquery / CTE / Window

**Q. `CASE` kya hai?**
SQL ka if-else. Pehla matching `WHEN` jeetta hai.

**Q. Pivot table kaise?**
`CASE` + aggregate + `GROUP BY`.

**Q. Correlated vs Non-correlated subquery?**
Non-correlated — independent, ek baar chalti hai
Correlated — outer query pe depend, **har row** ke liye chalti hai (slow)

**Q. 2nd highest salary?** 🔥
```sql
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- ya
SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;
```

**Q. Nth highest?**
`ORDER BY salary DESC LIMIT 1 OFFSET (N-1)`

**Q. CTE kya hai?**
`WITH` se banaya temporary named result set. Subquery se zyada readable, recursion support karta hai.

**Q. CTE vs Temp table vs View?**
CTE — memory me, query ke baad gayab
Temp table — session tak, index laga sakte ho
View — permanently saved query

**Q. Window function kya hai?**
Rows ke set pe calculation **bina rows collapse kiye**. `GROUP BY` rows squeeze karta hai, window nahi.

**Q. `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`?** 🔥
Scores 100, 90, 90, 80:
```
ROW_NUMBER -> 1, 2, 3, 4    (hamesha unique)
RANK       -> 1, 2, 2, 4    (tie pe GAP)
DENSE_RANK -> 1, 2, 2, 3    (tie pe gap NAHI)
```

**Q. `PARTITION BY` vs `GROUP BY`?**
`GROUP BY` — rows collapse, ek row per group
`PARTITION BY` — rows same rehti hain, bas window define hoti hai

**Q. `LAG` vs `LEAD`?**
`LAG` — pichli row. `LEAD` — agli row. Growth % ke liye.

**Q. Running total?**
`SUM(amount) OVER (ORDER BY date)`

**Q. Top N per group?**
`ROW_NUMBER()`/`RANK()` with `PARTITION BY`, phir CTE me `WHERE rnk <= N`.
(Window function `WHERE` me directly nahi likh sakte!)

---

## Transactions + Security 🔴

**Q. Transaction kya hai?**
SQL statements ka group jo ek unit ki tarah chalta hai. Ya sab commit, ya sab rollback.

**Q. ACID?**
**A**tomicity — sab ya kuch nahi
**C**onsistency — valid state se valid state
**I**solation — transactions ek doosre ko disturb na karein
**D**urability — commit ke baad data pakka

**Q. SQL Injection kya hai?** 🔥
Attacker user input ke through SQL code inject karta hai. Data chura sakta hai, delete kar sakta hai, login bypass kar sakta hai.
```
Input:  admin' --
Query:  SELECT * FROM users WHERE username = 'admin' --'
        ^^ password check ud gaya
```

**Q. SQL Injection se kaise bachein?** 🔥
**Parameterized queries** — `?` (SQLite) ya `%s` (MySQL). Kabhi string concatenation se query mat banao. ORM use karo (Django ORM safe hai).

**Q. Parameterized query kaam kaise karti hai?**
Query ka **structure** pehle compile hota hai, input baad me sirf **data** ki tarah bind hota hai. Input kabhi code nahi ban sakta.

**Q. Deadlock kya hai?**
Do transactions ek doosre ka lock wait kar rahe hain. DB ek ko kill kar deta hai. Bachne ke liye: same order me lock lo, transactions chhote rakho.

**Q. Isolation levels?**
`READ UNCOMMITTED` < `READ COMMITTED` < `REPEATABLE READ` < `SERIALIZABLE`

---

# 🗃️ DATABASE

**Q. DBMS vs RDBMS?**
DBMS — data store karta hai. RDBMS — tables me + relationships + ACID.

**Q. Primary Key vs Unique Key?**
| | Primary Key | Unique Key |
|---|---|---|
| NULL | ❌ | ✅ (ek) |
| Kitne | 1 per table | Kitne bhi |

**Q. Foreign Key kya karta hai?**
Relationship banata hai + referential integrity enforce karta hai.

**Q. `ON DELETE CASCADE` vs `SET NULL` vs `RESTRICT`?**
`CASCADE` — child rows bhi delete
`SET NULL` — child ka FK NULL
`RESTRICT` — delete hone hi nahi dega

**Q. Composite key?**
2+ columns milke primary key (junction table me common).

**Q. Normalization kyun?**
Redundancy hatao, insert/update/delete anomalies roko.

**Q. 1NF, 2NF, 3NF?**
1NF — atomic values
2NF — 1NF + no partial dependency
3NF — 2NF + no transitive dependency

**Q. Denormalization kab?**
Performance ke liye jaan bujh ke duplicate rakhna (JOIN kam karne ke liye). Reporting/analytics me.

**Q. Index kya hai? Trade-off?**
Fast lookup structure. SELECT fast, INSERT/UPDATE slow, extra disk space.

**Q. Index kab NAHI lagana?**
Chhoti tables, bahut update hone wale columns, low cardinality (gender).

**Q. Relationships ke types?**
1:1 (UNIQUE FK), 1:N (FK "many" side pe), M:N (junction table).

**Q. `CHAR` vs `VARCHAR`?**
`CHAR(n)` fixed length, `VARCHAR(n)` variable. Zyadatar VARCHAR.

**Q. Paise ke liye kaunsa data type?**
`DECIMAL`. **`FLOAT` kabhi nahi** — rounding errors.

---

# 🔗 PYTHON + DATABASE

**Q. Python se database kaise connect karte ho?** 🔥
```
Connection → Cursor → Execute → Fetch → Commit → Close
```
```python
conn = mysql.connector.connect(host=..., user=..., password=..., database=...)
cursor = conn.cursor()
cursor.execute("SELECT * FROM employees WHERE id = %s", (1,))
rows = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()
```

**Q. Cursor kya hai?**
Object jo queries execute karta hai aur results traverse karta hai.

**Q. `fetchone` vs `fetchall` vs `fetchmany`?**
`fetchone()` — ek row
`fetchall()` — saari rows
`fetchmany(n)` — n rows (badi data ke liye)

**Q. `commit()` kab zaroori hai?**
INSERT / UPDATE / DELETE ke baad. SELECT me nahi.

**Q. `executemany()` kya karta hai?**
Bulk insert — ek-ek karke insert karne se bahut fast.

**Q. Connection close kyun zaroori hai?**
Resources free hote hain. Warna connection pool exhaust ho jaayega.

**Q. Placeholder kya hai?**
SQLite `?`, MySQL/PostgreSQL `%s`. SQL injection se bachata hai.

---

# 🐙 GIT

**Q. Git vs GitHub?**
Git — distributed version control software (local). GitHub — cloud hosting + collaboration platform.

**Q. `git fetch` vs `git pull`?**
`fetch` — download only. `pull` = `fetch` + `merge`.

**Q. `git merge` vs `git rebase`?**
`merge` — merge commit banata hai, history branched (safe)
`rebase` — history linear banata hai (saaf, par rewrite karta hai)
**Shared branch pe kabhi rebase mat karo.**

**Q. `git reset` vs `git revert`?**
`reset` — history se commit hatata hai (private branch)
`revert` — ulta commit banata hai (public branch — safe)

**Q. Staging area kya hai?**
Working directory aur commit ke beech ka buffer.

**Q. `HEAD` kya hai?**
Current branch ke latest commit ka pointer.

**Q. Merge conflict kab?**
Jab do branches me same file ki same line badli ho.

**Q. Pull Request kya hai?**
Code review ke liye request. Merge se pehle team review karti hai.

**Q. `git stash`?**
Incomplete changes temporarily side me rakhta hai.

**Q. `.gitignore` me kya daalo?**
`venv/`, `__pycache__/`, `.env`, `*.db`, `node_modules/`, IDE files.

---

# 💡 BEHAVIOURAL (HR Round)

**Q. Apne baare me batao?**
> "Main [naam], BCA graduate. Python full stack development pe focus kar raha hoon — Django backend, REST APIs, aur React frontend. Maine ek Employee Management System banaya hai Python aur MySQL se, jisme poora CRUD, parameterized queries for SQL injection safety, aur transaction handling hai. Abhi Django REST Framework pe kaam kar raha hoon. Backend development me career banana chahta hoon."

**Q. Apna project batao?**
STAR method use karo:
- **Situation** — kya problem thi
- **Task** — tumhara role kya tha
- **Action** — kya banaya, kaunsi tech
- **Result** — kya achieve hua, kya seekha

**Q. Tumhari strength?**
Ek strength + example do. "Problem solving — jab EMS me SQL injection ka issue samjha, maine poora code parameterized queries pe migrate kiya aur 4 attack scenarios ke tests likhe."

**Q. Weakness?**
Real weakness + kya kar rahe ho uske liye. "Testing pe pehle dhyan nahi deta tha. Ab har project me tests likhta hoon — mere EMS project me 71 automated tests hain."

**Q. 5 saal baad kahan?**
"Senior backend developer banna chahta hoon jo system design kar sake aur juniors ko mentor kar sake."

**Q. Koi question hai hamare liye?** (HAMESHA POOCHHO)
- "Team ka tech stack kya hai?"
- "Naye joinee ka onboarding kaisa hota hai?"
- "Pehle 3 mahine me mujhse kya expect kiya jaayega?"
- "Code review process kaisa hai?"

---

# 🚨 Last-Minute Cheat Sheet

Interview se 10 minute pehle ye dekh lo:

| Topic | One-liner |
|---|---|
| OOP 4 pillars | Encapsulation, Inheritance, Polymorphism, Abstraction |
| `*args` / `**kwargs` | tuple / dict |
| `WHERE` vs `HAVING` | rows / groups |
| `COUNT(*)` vs `COUNT(col)` | sab rows / non-NULL |
| JOIN types | INNER, LEFT, RIGHT, FULL, SELF, CROSS |
| 2nd highest | `MAX` where `< MAX`, ya `LIMIT 1 OFFSET 1` |
| RANK vs DENSE_RANK | gap hai / gap nahi |
| ACID | Atomicity, Consistency, Isolation, Durability |
| SQL Injection fix | Parameterized queries (`?` / `%s`) |
| Normalization | 1NF atomic, 2NF no partial, 3NF no transitive |
| DB flow | Connection → Cursor → Execute → Fetch → Commit → Close |
| `git reset` vs `revert` | private / public branch |
