"""
================================================================
RUN ALL CHECKS — sab kuch chal raha hai ya nahi
================================================================
Chalao:  python3 run_all_checks.py     (MASTERY folder ke andar se)

Ye har Python script aur har SQL file chala ke check karta hai.
Kuch tod diya to yahan pata chal jaayega.
================================================================
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

PYTHON_SCRIPTS = [
    "phase1_python/step01_basics.py",
    "phase1_python/step02_functions.py",
    "phase1_python/step03_oop.py",
    "phase1_python/step04_exceptions.py",
    "phase1_python/step05_files_json.py",
    "phase1_python/step06_modules/main.py",
    "phase1_python/step07_libraries.py",
    "phase1_python/exercises/solutions.py",
    "phase2_sql/setup_db.py",
    "phase2_sql/transactions_demo.py",
    "phase4_python_db/ems/database.py",
    "phase4_python_db/ems/test_ems.py",
]

SQL_FILES = [
    "phase2_sql/step09_basics.sql",
    "phase2_sql/step10_filtering.sql",
    "phase2_sql/step11_aggregates.sql",
    "phase2_sql/step12_joins.sql",
    "phase2_sql/step13_case.sql",
    "phase2_sql/step14_subqueries.sql",
    "phase2_sql/step15_cte.sql",
    "phase2_sql/step16_window_functions.sql",
    "phase2_sql/step17_transactions_security.sql",
    "phase2_sql/solutions/all_solutions.sql",
]

# Ye SQL files me jaan bujh ke errors hain (demo ke liye)
EXPECTED_ERRORS = {
    "phase2_sql/step17_transactions_security.sql": 1,   # CHECK constraint demo
}

passed = 0
failed = 0
results = []


def run_python(script):
    global passed, failed
    path = ROOT / script
    if not path.exists():
        failed += 1
        results.append(("❌", script, "file nahi mili"))
        return

    proc = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True, text=True, timeout=120,
        cwd=str(path.parent),
    )
    if proc.returncode == 0:
        passed += 1
        lines = len(proc.stdout.strip().split("\n"))
        results.append(("✅", script, f"{lines} lines output"))
    else:
        failed += 1
        err = (proc.stderr.strip().split("\n")[-1] if proc.stderr else "unknown")[:60]
        results.append(("❌", script, err))


def run_sql(sql_file):
    global passed, failed
    path = ROOT / sql_file
    if not path.exists():
        failed += 1
        results.append(("❌", sql_file, "file nahi mili"))
        return

    proc = subprocess.run(
        [sys.executable, str(ROOT / "phase2_sql/run_sql.py"), str(path)],
        capture_output=True, text=True, timeout=120, cwd=str(ROOT),
    )
    error_count = proc.stdout.count("❌ ERROR")
    expected = EXPECTED_ERRORS.get(sql_file, 0)

    if proc.returncode == 0 and error_count == expected:
        passed += 1
        note = f"OK ({expected} expected error)" if expected else "OK"
        results.append(("✅", sql_file, note))
    else:
        failed += 1
        results.append(("❌", sql_file, f"{error_count} errors (expected {expected})"))


def main():
    print("=" * 74)
    print("  MASTERY — RUN ALL CHECKS")
    print("=" * 74)

    print("\n  [1/3] Database setup...")
    subprocess.run([sys.executable, str(ROOT / "phase2_sql/setup_db.py")],
                   capture_output=True, cwd=str(ROOT))
    print("        done")

    print("\n  [2/3] Python scripts...")
    for script in PYTHON_SCRIPTS:
        run_python(script)

    print("  [3/3] SQL files...")
    for sql_file in SQL_FILES:
        run_sql(sql_file)

    print("\n" + "=" * 74)
    print(f"  {'':<3} {'FILE':<48} {'RESULT'}")
    print("  " + "-" * 70)
    for status, name, note in results:
        print(f"  {status}  {name:<48} {note}")

    print("\n" + "=" * 74)
    total = passed + failed
    if failed == 0:
        print(f"  ✅ SAB THEEK — {passed}/{total} files chal rahi hain")
    else:
        print(f"  ❌ {failed} FAIL, {passed} PASS  (total {total})")
    print("=" * 74 + "\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
