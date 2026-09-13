"""
================================================================
STEP 17 — TRANSACTIONS + SQL INJECTION (LIVE DEMO)
================================================================
Chalao:  python3 phase2_sql/transactions_demo.py

Yahan tu ACTUALLY dekhega:
  - ROLLBACK se paisa wapas aata hua
  - SQL Injection se table DELETE hoti hui
  - Parameterized query se attack fail hota hua

Ye demo apna alag temp database use karta hai.
================================================================
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "transactions_demo.db"


def fresh_db():
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    conn.executescript("""
        CREATE TABLE accounts (
            id      INTEGER PRIMARY KEY,
            owner   TEXT NOT NULL,
            balance INTEGER NOT NULL CHECK (balance >= 0)
        );
        INSERT INTO accounts VALUES (1, 'Noman', 10000), (2, 'Ali', 5000);

        CREATE TABLE users (
            id       INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role     TEXT
        );
        INSERT INTO users VALUES
            (1, 'admin', 'admin@123',  'administrator'),
            (2, 'noman', 'noman@456',  'user'),
            (3, 'ali',   'ali@789',    'user');
    """)
    conn.commit()
    return conn


def show_accounts(conn, label):
    rows = conn.execute("SELECT id, owner, balance FROM accounts ORDER BY id").fetchall()
    print(f"    {label}")
    for r in rows:
        print(f"      {r[0]}. {r[1]:<6} balance = {r[2]:>7}")


# ==============================================================
# DEMO 1: SUCCESSFUL TRANSACTION (COMMIT)
# ==============================================================

def demo_commit():
    print("\n" + "=" * 62)
    print("DEMO 1: SUCCESSFUL TRANSFER (COMMIT)")
    print("=" * 62)

    conn = fresh_db()
    show_accounts(conn, "PEHLE:")

    print("\n    Noman -> Ali, 2000 transfer")
    try:
        conn.execute("BEGIN")
        conn.execute("UPDATE accounts SET balance = balance - 2000 WHERE id = 1")
        conn.execute("UPDATE accounts SET balance = balance + 2000 WHERE id = 2")
        conn.commit()
        print("    ✅ COMMIT — transfer successful")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"    ❌ ROLLBACK: {e}")

    show_accounts(conn, "\n    BAAD ME:")
    conn.close()


# ==============================================================
# DEMO 2: FAILED TRANSACTION (ROLLBACK) — asli power
# ==============================================================

def demo_rollback():
    print("\n" + "=" * 62)
    print("DEMO 2: FAILED TRANSFER (ROLLBACK) 🔥")
    print("=" * 62)

    conn = fresh_db()
    show_accounts(conn, "PEHLE:")

    print("\n    Noman -> Ali, 50000 transfer (Noman ke paas sirf 10000 hai)")
    try:
        conn.execute("BEGIN")

        conn.execute("UPDATE accounts SET balance = balance - 50000 WHERE id = 1")
        print("    Step 1: Noman se 50000 kaata... (abhi commit nahi hua)")

        conn.execute("UPDATE accounts SET balance = balance + 50000 WHERE id = 2")
        print("    Step 2: Ali ko 50000 diya...")

        conn.commit()
        print("    ✅ COMMIT")

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"    ❌ ERROR: {e}")
        print("    🔄 ROLLBACK kiya — sab changes cancel")

    show_accounts(conn, "\n    BAAD ME:")
    print("\n    👆 Balance BILKUL same hai. Paisa gayab nahi hua.")
    print("       Bina transaction ke Noman ka paisa kat jaata aur")
    print("       Ali ko milta hi nahi. YE HAI TRANSACTION KI POWER.")
    conn.close()


# ==============================================================
# DEMO 3: SAVEPOINT
# ==============================================================

def demo_savepoint():
    print("\n" + "=" * 62)
    print("DEMO 3: SAVEPOINT (partial rollback)")
    print("=" * 62)

    conn = fresh_db()
    show_accounts(conn, "PEHLE:")

    conn.execute("BEGIN")

    conn.execute("UPDATE accounts SET balance = balance + 1000 WHERE id = 1")
    print("\n    Noman ko 1000 bonus diya")

    conn.execute("SAVEPOINT after_bonus")
    print("    📌 SAVEPOINT 'after_bonus' bana")

    conn.execute("UPDATE accounts SET balance = balance - 3000 WHERE id = 1")
    conn.execute("UPDATE accounts SET balance = balance - 3000 WHERE id = 2")
    print("    Dono se 3000 kaata (galti se)")

    conn.execute("ROLLBACK TO after_bonus")
    print("    🔄 ROLLBACK TO after_bonus — sirf deduction cancel")

    conn.commit()
    show_accounts(conn, "\n    BAAD ME:")
    print("\n    👆 Bonus bacha (+1000), deduction cancel ho gaya")
    conn.close()


# ==============================================================
# DEMO 4: SQL INJECTION — ATTACK 💀
# ==============================================================

def demo_sql_injection_attack():
    print("\n" + "=" * 62)
    print("DEMO 4: SQL INJECTION — ATTACK 💀 (GALAT TAREEKA)")
    print("=" * 62)

    conn = fresh_db()

    def vulnerable_login(username, password):
        """❌ KABHI AISA MAT LIKHNA — string concatenation"""
        query = (f"SELECT * FROM users WHERE username = '{username}' "
                 f"AND password = '{password}'")
        print(f"      Query: {query}")
        try:
            return conn.execute(query).fetchall()
        except sqlite3.Error as e:
            return f"Error: {e}"

    print("\n  ✅ Normal login:")
    print("      username='noman', password='noman@456'")
    result = vulnerable_login("noman", "noman@456")
    print(f"      Result: {result}")

    print("\n  ❌ Galat password:")
    result = vulnerable_login("noman", "wrongpass")
    print(f"      Result: {result}  <- login fail, sahi hai")

    print("\n  💀 ATTACK 1 — Comment injection (password bypass):")
    print("      username=\"admin' --\"  password=\"kuch bhi\"")
    result = vulnerable_login("admin' --", "kuch bhi")
    print(f"      Result: {result}")
    print("      👆 BINA PASSWORD ke admin ka data mil gaya!")

    print("\n  💀 ATTACK 2 — OR 1=1 (saare users):")
    print("      username=\"' OR '1'='1\"  password=\"' OR '1'='1\"")
    result = vulnerable_login("' OR '1'='1", "' OR '1'='1")
    print(f"      Result: {len(result) if isinstance(result, list) else result} users mile")
    print("      👆 POORA DATABASE leak ho gaya!")

    print("\n  💀 ATTACK 3 — DROP TABLE:")
    print("      username=\"'; DROP TABLE users; --\"")
    try:
        conn.executescript(
            "SELECT * FROM users WHERE username = ''; DROP TABLE users; --'"
        )
        print("      👆 TABLE DELETE HO GAYI 💀💀💀")
        try:
            conn.execute("SELECT * FROM users").fetchall()
        except sqlite3.Error as e:
            print(f"      Check: {e}")
    except sqlite3.Error as e:
        print(f"      {e}")

    conn.close()


# ==============================================================
# DEMO 5: PARAMETERIZED QUERY — DEFENSE ✅
# ==============================================================

def demo_parameterized_defense():
    print("\n" + "=" * 62)
    print("DEMO 5: PARAMETERIZED QUERY — DEFENSE ✅ (SAHI TAREEKA)")
    print("=" * 62)

    conn = fresh_db()

    def safe_login(username, password):
        """✅ AISA LIKHNA — placeholder ke saath"""
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        print(f"      Query: {query}")
        print(f"      Params: ({username!r}, {password!r})")
        return conn.execute(query, (username, password)).fetchall()

    print("\n  ✅ Normal login:")
    result = safe_login("noman", "noman@456")
    print(f"      Result: {result}")

    print("\n  🛡️  ATTACK 1 try karo — Comment injection:")
    result = safe_login("admin' --", "kuch bhi")
    print(f"      Result: {result}")
    print("      👆 ATTACK FAIL! Input ko sirf TEXT samjha gaya.")

    print("\n  🛡️  ATTACK 2 try karo — OR 1=1:")
    result = safe_login("' OR '1'='1", "' OR '1'='1")
    print(f"      Result: {result}")
    print("      👆 ATTACK FAIL! 0 rows.")

    print("\n  🛡️  ATTACK 3 try karo — DROP TABLE:")
    result = safe_login("'; DROP TABLE users; --", "x")
    print(f"      Result: {result}")
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    print(f"      Table abhi bhi zinda hai: {count} users")
    print("      👆 ATTACK FAIL! Table safe.")

    print("""
  KYUN KAAM KARTA HAI?
    Database pehle query ka STRUCTURE compile karta hai:
        SELECT * FROM users WHERE username = ? AND password = ?
    Phir ? ki jagah value sirf DATA ki tarah bind hoti hai.
    User ka input kabhi SQL CODE nahi ban sakta. Bas itna simple.
    """)

    conn.close()


# ==============================================================
# DEMO 6: PLACEHOLDER KE RULES
# ==============================================================

def demo_placeholder_rules():
    print("\n" + "=" * 62)
    print("DEMO 6: PLACEHOLDER KE RULES (common galtiyan)")
    print("=" * 62)

    conn = fresh_db()

    print("\n  ✅ SQLite -> ?      |  MySQL -> %s   |  PostgreSQL -> %s")

    print("\n  ✅ Single value — TUPLE bhejo (comma dhyan se!):")
    r = conn.execute("SELECT username FROM users WHERE id = ?", (1,)).fetchone()
    print(f"      execute('... = ?', (1,))  ->  {r}")

    print("\n  ❌ Comma bhool gaye to error:")
    try:
        conn.execute("SELECT * FROM users WHERE id = ?", (1))
    except (sqlite3.Error, TypeError) as e:
        print(f"      execute('... = ?', (1))  ->  {type(e).__name__}: {e}")

    print("\n  ✅ Multiple values:")
    rows = conn.execute(
        "SELECT username, role FROM users WHERE role = ? AND id > ?",
        ("user", 1)
    ).fetchall()
    print(f"      {rows}")

    print("\n  ✅ LIKE ke saath (% value me daalo, query me nahi):")
    rows = conn.execute(
        "SELECT username FROM users WHERE username LIKE ?", ("%a%",)
    ).fetchall()
    print(f"      LIKE ? with '%a%'  ->  {rows}")

    print("\n  ✅ IN clause (dynamic placeholders):")
    ids = [1, 3]
    placeholders = ",".join("?" * len(ids))
    rows = conn.execute(
        f"SELECT username FROM users WHERE id IN ({placeholders})", ids
    ).fetchall()
    print(f"      IN ({placeholders}) with {ids}  ->  {rows}")

    print("\n  ✅ Named placeholders (zyada readable):")
    rows = conn.execute(
        "SELECT username FROM users WHERE role = :role",
        {"role": "administrator"}
    ).fetchall()
    print(f"      :role  ->  {rows}")

    print("\n  ❌ TABLE/COLUMN NAME placeholder se NAHI aata:")
    print("      conn.execute('SELECT * FROM ?', ('users',))   <- kaam nahi karega")
    print("\n  ✅ Uske liye WHITELIST banao:")
    print("""      ALLOWED_TABLES = {"users", "accounts"}
      if table not in ALLOWED_TABLES:
          raise ValueError("Invalid table name")
      conn.execute(f"SELECT * FROM {table}")""")

    print("\n  ✅ executemany — bulk insert (fast + safe):")
    data = [(10, "test1", "p1", "user"), (11, "test2", "p2", "user")]
    conn.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", data)
    conn.commit()
    print(f"      {conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]} users total")

    conn.close()


if __name__ == "__main__":
    print("=" * 62)
    print("TRANSACTIONS + SQL INJECTION — LIVE DEMO")
    print("=" * 62)

    demo_commit()
    demo_rollback()
    demo_savepoint()
    demo_sql_injection_attack()
    demo_parameterized_defense()
    demo_placeholder_rules()

    if DB.exists():
        DB.unlink()

    print("\n" + "=" * 62)
    print("YAAD RAKHNE WALI 3 BAATEIN")
    print("=" * 62)
    print("""
  1. Paise/critical data wale operations me HAMESHA transaction use karo.
     try -> execute -> commit  /  except -> rollback

  2. Query me user input KABHI concatenate mat karo.
     Hamesha placeholder: ? (SQLite) ya %s (MySQL)

  3. Django ORM use karoge to injection se automatically safe ho.
     Par raw SQL likhte waqt khud dhyan rakhna padega.
    """)
