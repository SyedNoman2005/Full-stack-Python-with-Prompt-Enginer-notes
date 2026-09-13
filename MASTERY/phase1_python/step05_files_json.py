"""
================================================================
STEP 5 — FILES + CSV + JSON  🔴🔴
================================================================
Chalane ke liye:  python3 phase1_python/step05_files_json.py

JSON = API ki language. Har REST API JSON bhejti/leti hai.
Ye step DRF (Django REST Framework) ki seedhi tayyari hai.

Sab files 'output/' folder me banti hain (gitignored).
================================================================
"""

import csv
import json
import os
from pathlib import Path

# Output folder — is script ke bagal me
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)


# ==============================================================
# 1. FILE MODES — pehle ye samajh
# ==============================================================
FILE_MODES = """
  MODE   MEANING                            File nahi hai to?   Purana data?
  ----   -------------------------------    -----------------   ------------
  'r'    read (default)                     ERROR               -
  'w'    write                              bana dega           MITA DEGA ⚠️
  'a'    append (end me jodo)               bana dega           bacha rahega
  'x'    exclusive create                   bana dega           ERROR agar hai
  'r+'   read + write                       ERROR               bacha rahega
  'rb'   read binary (image, pdf)           ERROR               -
  'wb'   write binary                       bana dega           MITA DEGA
"""


# ==============================================================
# 2. TEXT FILE — write, read, append
# ==============================================================

def text_file_demo():
    print("\n--- 2. TEXT FILES ---")
    print(FILE_MODES)

    path = OUT / "employees.txt"

    # WRITE — 'w' purana sab mita deta hai
    print("  [WRITE]")
    with open(path, "w", encoding="utf-8") as f:
        f.write("Noman,30000,IT\n")
        f.write("Ali,45000,HR\n")
        f.writelines(["Sara,52000,IT\n", "Zoya,38000,Sales\n"])
    print(f"    4 employees likhe -> {path.name}")

    # APPEND — 'a' end me jodta hai
    print("\n  [APPEND]")
    with open(path, "a", encoding="utf-8") as f:
        f.write("Imran,41000,HR\n")
    print("    1 employee add kiya")

    # READ — poori file ek saath
    print("\n  [READ — read()]")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"    Total characters: {len(content)}")

    # READ — line by line (BADI FILES KE LIYE YEHI SAHI HAI)
    print("\n  [READ — line by line, memory efficient]")
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            name, salary, dept = line.strip().split(",")
            print(f"    {i}. {name:<6} {salary:>6}  {dept}")

    # READ — readlines() -> list
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"\n  [readlines()] -> list of {len(lines)} lines")

    print("\n  'with' KYUN use karein?")
    print("    File automatically band ho jaati hai — error aaye tab bhi.")
    print("    Bina 'with': f = open(...); f.close() khud likhna padta hai,")
    print("    aur error aaya to close hi nahi hoga.")

    # PROGRAM 1 (tera task): employee data text file me save karo
    print("\n  [PROGRAM 1] Employee data text file me save — DONE ✓")


# ==============================================================
# 3. CSV FILES — Excel/data ka standard
# ==============================================================

def csv_demo():
    print("\n--- 3. CSV FILES ---")

    path = OUT / "employees.csv"

    employees = [
        {"id": 1, "name": "Noman", "salary": 30000, "dept": "IT"},
        {"id": 2, "name": "Ali", "salary": 45000, "dept": "HR"},
        {"id": 3, "name": "Sara", "salary": 52000, "dept": "IT"},
        {"id": 4, "name": "Zoya", "salary": 38000, "dept": "Sales"},
    ]

    # WRITE with DictWriter — sabse aasan tareeka
    print("  [WRITE — DictWriter]")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "salary", "dept"])
        writer.writeheader()
        writer.writerows(employees)
    print(f"    {len(employees)} rows likhe -> {path.name}")
    print("    NOTE: newline='' zaroori hai, warna Windows pe blank lines aayengi")

    # READ with DictReader — har row dict banti hai
    print("\n  [READ — DictReader]")
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        print(f"    {row['id']}. {row['name']:<6} {row['salary']:>6}  {row['dept']}")

    print("\n    ⚠️  CSV se sab STRING aata hai. Number chahiye to int() karo.")
    total = sum(int(r["salary"]) for r in rows)
    print(f"    Total salary = {total}")
    print(f"    Average      = {total / len(rows):.2f}")

    # Filtering — Pandas se pehle ka tareeka
    print("\n  [FILTER] IT department:")
    for r in rows:
        if r["dept"] == "IT":
            print(f"    {r['name']} — {r['salary']}")

    # Basic csv.reader / writer (list based)
    print("\n  [csv.reader — list based]")
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)           # pehli line header hai
        print(f"    header = {header}")
        print(f"    first row = {next(reader)}")


# ==============================================================
# 4. JSON — API ki language  🔴🔴🔴
# ==============================================================

def json_demo():
    print("\n--- 4. JSON (API ki language) ---")

    print("""
  CHAAR FUNCTIONS — ye confuse hote hain, clear kar lo:

    json.dump(obj, file)   -> Python object  -> FILE me likho
    json.load(file)        -> FILE se padho  -> Python object
    json.dumps(obj)        -> Python object  -> STRING
    json.loads(string)     -> STRING         -> Python object

    's' ka matlab = STRING.  's' nahi = FILE.
    """)

    path = OUT / "employees.json"

    data = {
        "company": "TechCorp",
        "location": "Hyderabad",
        "employees": [
            {"id": 1, "name": "Noman", "salary": 30000, "dept": "IT",
             "skills": ["Python", "SQL"], "active": True},
            {"id": 2, "name": "Ali", "salary": 45000, "dept": "HR",
             "skills": ["Communication"], "active": True},
            {"id": 3, "name": "Sara", "salary": 52000, "dept": "IT",
             "skills": ["Django", "React", "SQL"], "active": False},
        ],
    }

    # ---- json.dump() — object se FILE ----
    print("  [json.dump] Python object -> file")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"    Likha -> {path.name}")

    # ---- json.load() — FILE se object  [PROGRAM 2] ----
    print("\n  [json.load] file -> Python object   (PROGRAM 2)")
    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    print(f"    Company   : {loaded['company']}")
    print(f"    Employees : {len(loaded['employees'])}")
    for e in loaded["employees"]:
        status = "Active" if e["active"] else "Inactive"
        print(f"      {e['name']:<6} {e['salary']:>6}  {e['dept']:<6} {status}")

    # ---- json.dumps() — object se STRING ----
    print("\n  [json.dumps] Python object -> string")
    single = {"name": "Noman", "salary": 30000}
    as_string = json.dumps(single)
    print(f"    {as_string}")
    print(f"    type = {type(as_string).__name__}")

    # ---- json.loads() — STRING se object ----
    print("\n  [json.loads] string -> Python object")
    api_response = '{"status": "success", "count": 3, "data": [1, 2, 3]}'
    parsed = json.loads(api_response)
    print(f"    parsed['status'] = {parsed['status']}")
    print(f"    parsed['data']   = {parsed['data']}")
    print(f"    type = {type(parsed).__name__}")
    print("    ^^ requests library me response.json() yahi karta hai")

    # ---- PROGRAM 3: JSON update karo ----
    print("\n  [PROGRAM 3] JSON data update karo")
    print("    Flow: load -> modify -> dump")

    with open(path, "r", encoding="utf-8") as f:
        db = json.load(f)

    # 1. Salary badhao
    for e in db["employees"]:
        if e["name"] == "Noman":
            old = e["salary"]
            e["salary"] = 35000
            print(f"    Noman ki salary: {old} -> {e['salary']}")

    # 2. Naya employee add karo
    db["employees"].append({
        "id": 4, "name": "Imran", "salary": 41000, "dept": "Sales",
        "skills": ["Negotiation"], "active": True,
    })
    print("    Imran add kiya")

    # 3. Employee delete karo
    db["employees"] = [e for e in db["employees"] if e["id"] != 3]
    print("    Sara (id 3) delete ki")

    # 4. Wapas save
    with open(path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)
    print(f"    Save kiya. Ab {len(db['employees'])} employees hain")


# ==============================================================
# 5. JSON <-> PYTHON TYPE MAPPING
# ==============================================================

def json_types_demo():
    print("\n--- 5. JSON <-> PYTHON TYPES ---")

    print("""
    PYTHON          JSON
    ------          ----
    dict            object   {}
    list, tuple     array    []
    str             string
    int, float      number
    True            true     <- chhota t !
    False           false
    None            null
    """)

    obj = {
        "text": "hello", "number": 42, "decimal": 3.14,
        "yes": True, "no": False, "nothing": None,
        "list": [1, 2, 3], "nested": {"a": 1},
    }
    print(f"  Python : {obj}")
    print(f"  JSON   : {json.dumps(obj)}")

    print("\n  JSON me jo NAHI chalta:")
    print("    - tuple  -> list ban jaata hai")
    print("    - set    -> ERROR (TypeError)")
    print("    - datetime -> ERROR (str() karo pehle)")
    print("    - custom object -> ERROR (dict me convert karo)")

    try:
        json.dumps({"s": {1, 2, 3}})
    except TypeError as e:
        print(f"\n  set try kiya -> TypeError: {e}")

    # Solution: default= parameter
    from datetime import datetime
    print("\n  datetime ka solution (default= use karo):")
    result = json.dumps({"now": datetime(2026, 1, 15)}, default=str)
    print(f"    {result}")


# ==============================================================
# 6. JSON ERROR HANDLING (Step 4 ka connection)
# ==============================================================

def json_errors_demo():
    print("\n--- 6. JSON ERROR HANDLING ---")

    def safe_load_json(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f), None
        except FileNotFoundError:
            return None, "File nahi mili"
        except json.JSONDecodeError as e:
            return None, f"Galat JSON format: {e.msg} (line {e.lineno})"
        except PermissionError:
            return None, "Permission nahi hai"

    # Test 1: sahi file
    data, err = safe_load_json(OUT / "employees.json")
    print(f"  Sahi file      -> {'OK, ' + str(len(data['employees'])) + ' employees' if data else err}")

    # Test 2: file nahi hai
    data, err = safe_load_json(OUT / "nahi_hai.json")
    print(f"  Missing file   -> {err}")

    # Test 3: kharab JSON
    bad = OUT / "bad.json"
    bad.write_text('{"name": "Noman", "salary": }', encoding="utf-8")
    data, err = safe_load_json(bad)
    print(f"  Kharab JSON    -> {err}")


# ==============================================================
# 7. MINI PROJECT — JSON as Database (CRUD)
# ==============================================================

class JsonDB:
    """
    JSON file ko chhota database banao.
    Ye EMS project ka chhota version hai — Phase 4 me DB ke saath karega.
    """

    def __init__(self, filepath):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self._save([])

    def _load(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, records):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)

    # CREATE
    def add(self, record):
        records = self._load()
        record["id"] = max([r["id"] for r in records], default=0) + 1
        records.append(record)
        self._save(records)
        return record

    # READ
    def all(self):
        return self._load()

    def get(self, record_id):
        return next((r for r in self._load() if r["id"] == record_id), None)

    def search(self, field, value):
        return [r for r in self._load()
                if str(value).lower() in str(r.get(field, "")).lower()]

    # UPDATE
    def update(self, record_id, **fields):
        records = self._load()
        for r in records:
            if r["id"] == record_id:
                r.update(fields)
                self._save(records)
                return r
        return None

    # DELETE
    def delete(self, record_id):
        records = self._load()
        filtered = [r for r in records if r["id"] != record_id]
        if len(filtered) == len(records):
            return False
        self._save(filtered)
        return True


def mini_project_demo():
    print("\n--- 7. MINI PROJECT: JSON Database (CRUD) ---")

    db = JsonDB(OUT / "db.json")
    db._save([])        # reset

    print("  [CREATE]")
    for emp in [
        {"name": "Noman", "salary": 30000, "dept": "IT"},
        {"name": "Ali", "salary": 45000, "dept": "HR"},
        {"name": "Sara", "salary": 52000, "dept": "IT"},
    ]:
        created = db.add(emp)
        print(f"    Added id={created['id']} {created['name']}")

    print("\n  [READ ALL]")
    for r in db.all():
        print(f"    {r['id']}. {r['name']:<6} {r['salary']:>6}  {r['dept']}")

    print("\n  [READ ONE]")
    print(f"    db.get(2) -> {db.get(2)}")

    print("\n  [SEARCH dept=IT]")
    for r in db.search("dept", "IT"):
        print(f"    {r['name']}")

    print("\n  [UPDATE]")
    print(f"    {db.update(1, salary=35000)}")

    print("\n  [DELETE]")
    print(f"    db.delete(3) -> {db.delete(3)}")
    print(f"    Bache: {[r['name'] for r in db.all()]}")


# ==============================================================
INTERVIEW = """
Q1. 'with' statement kyun use karte hain?
    Context manager hai. File automatically close hoti hai —
    exception aaye tab bhi. Manually f.close() nahi likhna padta.

Q2. 'w' aur 'a' mode me fark?
    'w' -> purana data MITA deta hai
    'a' -> end me jodta hai, purana bacha rehta hai

Q3. read() vs readline() vs readlines()?
    read()      -> poori file ek string me
    readline()  -> ek line
    readlines() -> saari lines ki list
    Badi file ke liye: 'for line in file' — memory efficient

Q4. json.load vs json.loads?
    load  -> FILE object se padhta hai
    loads -> STRING se padhta hai ('s' = string)

Q5. json.dump vs json.dumps?
    dump  -> FILE me likhta hai
    dumps -> STRING return karta hai

Q6. JSON kyun important hai?
    REST API ki standard language. Har API JSON me data bhejti hai.
    Language-independent — Python, JS, Java sab samajhte hain.

Q7. Python set ko JSON me kyun nahi daal sakte?
    JSON me set type hi nahi hai. TypeError aayegi.
    Solution: list(my_set) kar do.

Q8. CSV me newline='' kyun likhte hain?
    Windows pe har row ke baad extra blank line aa jaati hai bina iske.

Q9. json.JSONDecodeError kab aati hai?
    Jab file ka content valid JSON nahi hota (comma missing, quote missing).

Q10. Bade JSON files kaise handle karein?
    Streaming parser (ijson) ya line-delimited JSON (JSONL) use karo.
    json.load() poori file memory me daal deta hai.
"""


PRACTICE = """
1.  Text file me 5 employees ka data likho. (PROGRAM 1)
2.  Usi file ko padh ke line by line print karo.
3.  File me naya employee append karo.
4.  CSV file banao aur DictWriter se 5 rows likho.
5.  CSV padh ke total aur average salary nikalo.
6.  JSON file banao nested data ke saath.
7.  JSON file padho aur specific employee dhoondho. (PROGRAM 2)
8.  JSON me salary update karo aur wapas save karo. (PROGRAM 3)
9.  JSON se employee delete karo.
10. JsonDB class ko extend karo — 'sort_by(field)' method add karo.
11. CSV ko JSON me convert karne wala script likho.
12. File na mile to proper error message do (crash mat hone do).
"""


if __name__ == "__main__":
    print("=" * 62)
    print("STEP 5 — FILES + CSV + JSON")
    print("=" * 62)

    text_file_demo()
    csv_demo()
    json_demo()
    json_types_demo()
    json_errors_demo()
    mini_project_demo()

    print("\n" + "=" * 62)
    print(f"Saari files yahan bani: {OUT}")
    print("Files:", ", ".join(sorted(p.name for p in OUT.iterdir())))
    print("=" * 62)

    print("\nINTERVIEW QUESTIONS")
    print("=" * 62)
    print(INTERVIEW)

    print("=" * 62)
    print("PRACTICE")
    print("=" * 62)
    print(PRACTICE)
