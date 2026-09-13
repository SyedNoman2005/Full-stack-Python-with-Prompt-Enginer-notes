"""
================================================================
SQL RUNNER — .sql files chalane ke liye
================================================================
Use:
  python3 phase2_sql/run_sql.py phase2_sql/step09_basics.sql   # file chalao
  python3 phase2_sql/run_sql.py                                # interactive mode
  python3 phase2_sql/run_sql.py -q "SELECT * FROM employees"   # ek query

Har query ka result table format me dikhta hai.
================================================================
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "practice.db"


def ensure_db():
    if not DB_PATH.exists():
        print("Database nahi mila. Pehle ye chalao:")
        print("  python3 phase2_sql/setup_db.py")
        sys.exit(1)


def print_table(cursor, max_rows=50):
    """Query result ko saaf table me dikhao."""
    rows = cursor.fetchall()

    if cursor.description is None:
        return

    headers = [d[0] for d in cursor.description]

    if not rows:
        print("    (0 rows)")
        return

    # Column widths
    widths = [len(h) for h in headers]
    for row in rows[:max_rows]:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val) if val is not None else "NULL"))
    widths = [min(w, 30) for w in widths]

    # Header
    line = "  | " + " | ".join(h[:w].ljust(w) for h, w in zip(headers, widths)) + " |"
    sep = "  +" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(sep)
    print(line)
    print(sep)

    # Rows
    for row in rows[:max_rows]:
        cells = []
        for val, w in zip(row, widths):
            s = "NULL" if val is None else str(val)
            cells.append(s[:w].ljust(w))
        print("  | " + " | ".join(cells) + " |")
    print(sep)

    shown = min(len(rows), max_rows)
    extra = f" (showing {shown})" if len(rows) > max_rows else ""
    print(f"    {len(rows)} row(s){extra}")


def split_statements(sql_text):
    """
    SQL file ko statements me todo, comments ko heading ki tarah rakhte hue.
    Returns: list of (comment_block, statement)
    """
    statements = []
    current_comments = []
    current_sql = []

    for raw_line in sql_text.split("\n"):
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            if not current_sql:
                current_comments.append("")
            continue

        if stripped.startswith("--"):
            if not current_sql:
                current_comments.append(stripped)
            continue

        current_sql.append(line)

        if stripped.endswith(";"):
            statements.append(("\n".join(current_comments), "\n".join(current_sql)))
            current_comments = []
            current_sql = []

    if current_sql:
        statements.append(("\n".join(current_comments), "\n".join(current_sql)))

    return statements


def run_file(filepath):
    ensure_db()
    path = Path(filepath)
    if not path.exists():
        print(f"File nahi mili: {filepath}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    cur = conn.cursor()

    print("=" * 70)
    print(f"RUNNING: {path.name}")
    print("=" * 70)

    statements = split_statements(path.read_text(encoding="utf-8"))

    for comments, sql in statements:
        if comments.strip():
            print()
            for c in comments.split("\n"):
                if c.strip():
                    print(c)

        print(f"\n  SQL> {sql.strip()}")
        try:
            cur.execute(sql)
            if sql.strip().upper().startswith("SELECT") or " RETURNING " in sql.upper():
                print_table(cur)
            else:
                print(f"    OK ({cur.rowcount} row(s) affected)")
        except sqlite3.Error as e:
            print(f"    ❌ ERROR: {e}")

    conn.close()
    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)


def run_query(query):
    ensure_db()
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    cur = conn.cursor()
    try:
        cur.execute(query)
        if cur.description:
            print_table(cur)
        else:
            conn.commit()
            print(f"OK ({cur.rowcount} rows affected)")
    except sqlite3.Error as e:
        print(f"❌ ERROR: {e}")
    conn.close()


def interactive():
    ensure_db()
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    cur = conn.cursor()

    print("=" * 70)
    print("SQL INTERACTIVE MODE")
    print("=" * 70)
    print("  Query likho aur Enter dabao (; optional)")
    print("  .tables   -> saari tables")
    print("  .schema X -> table ka structure")
    print("  exit      -> bahar niklo")
    print("=" * 70)

    while True:
        try:
            q = input("\nSQL> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not q:
            continue
        if q.lower() in ("exit", "quit", ".exit", ".quit"):
            print("Bye!")
            break

        if q == ".tables":
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            print("  " + ", ".join(r[0] for r in cur.fetchall()))
            continue

        if q.startswith(".schema"):
            parts = q.split()
            if len(parts) > 1:
                cur.execute(
                    "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
                    (parts[1],))
                row = cur.fetchone()
                print(row[0] if row else "  Table nahi mili")
            continue

        try:
            cur.execute(q.rstrip(";"))
            if cur.description:
                print_table(cur)
            else:
                conn.commit()
                print(f"  OK ({cur.rowcount} rows affected)")
        except sqlite3.Error as e:
            print(f"  ❌ ERROR: {e}")

    conn.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive()
    elif sys.argv[1] in ("-q", "--query"):
        run_query(" ".join(sys.argv[2:]))
    else:
        run_file(sys.argv[1])
