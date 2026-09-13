"""
================================================================
STEP 7 — USEFUL LIBRARIES  🔴🔴
================================================================
Chalane ke liye:  python3 phase1_python/step07_libraries.py

os · pathlib · datetime · json · csv · re · requests · logging

SABSE IMPORTANT: requests
Yahin se tu API + Backend world me enter karega.

NOTE: requests install nahi hai to script crash nahi hogi —
      code dikha dega aur skip kar degi.
      Install karne ke liye:  pip install requests
================================================================
"""

import csv
import json
import logging
import os
import re
from datetime import datetime, timedelta, date
from pathlib import Path

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)


# ==============================================================
# 1. os — operating system ke saath baat
# ==============================================================

def os_demo():
    print("\n--- 1. os MODULE ---")

    print(f"  os.getcwd()            = {os.getcwd()}")
    print(f"  os.name                = {os.name}   (posix=Linux/Mac, nt=Windows)")
    print(f"  os.sep                 = '{os.sep}'     (path separator)")

    print("\n  os.path (paths ke saath kaam):")
    p = "/home/user/project/app.py"
    print(f"    basename  = {os.path.basename(p)}")
    print(f"    dirname   = {os.path.dirname(p)}")
    print(f"    splitext  = {os.path.splitext(p)}")
    print(f"    join      = {os.path.join('folder', 'sub', 'file.txt')}")
    print(f"    exists    = {os.path.exists(p)}")

    print("\n  Directory operations:")
    demo_dir = OUT / "os_demo"
    os.makedirs(demo_dir, exist_ok=True)         # exist_ok -> error nahi dega
    print(f"    makedirs('{demo_dir.name}')  -> bana diya")

    (demo_dir / "a.txt").write_text("A")
    (demo_dir / "b.txt").write_text("B")
    print(f"    listdir  -> {sorted(os.listdir(demo_dir))}")

    print("\n  ENVIRONMENT VARIABLES (secrets yahan rakhte hain):")
    print(f"    os.environ.get('HOME')       = {os.environ.get('HOME')}")
    print(f"    os.environ.get('SECRET_KEY') = {os.environ.get('SECRET_KEY', 'set nahi hai')}")
    print("    ^^ Django me SECRET_KEY, DB password yahin se aate hain.")
    print("       Code me password HARDCODE mat karna — .env file use karo.")


# ==============================================================
# 2. pathlib — os.path ka MODERN replacement
# ==============================================================

def pathlib_demo():
    print("\n--- 2. pathlib (MODERN — ye use karo) ---")

    p = Path("/home/user/project/app.py")

    print(f"  Path object  = {p}")
    print(f"  .name        = {p.name}")
    print(f"  .stem        = {p.stem}")
    print(f"  .suffix      = {p.suffix}")
    print(f"  .parent      = {p.parent}")
    print(f"  .parts       = {p.parts}")

    print("\n  / operator se path jodo (bahut saaf hai):")
    print(f"    Path('folder') / 'sub' / 'file.txt'  = {Path('folder') / 'sub' / 'file.txt'}")

    print("\n  Read/write ek line me:")
    f = OUT / "pathlib_test.txt"
    f.write_text("Hello from pathlib\n", encoding="utf-8")
    print(f"    write_text() -> done")
    print(f"    read_text()  -> {f.read_text(encoding='utf-8').strip()}")

    print("\n  Checks:")
    print(f"    f.exists()   = {f.exists()}")
    print(f"    f.is_file()  = {f.is_file()}")
    print(f"    f.is_dir()   = {f.is_dir()}")
    print(f"    f.stat().st_size = {f.stat().st_size} bytes")

    print("\n  Files dhoondho (glob):")
    py_files = sorted(Path(__file__).parent.glob("*.py"))
    for pf in py_files[:5]:
        print(f"    {pf.name}")

    print("\n  os.path vs pathlib:")
    print("    os.path.join(a, b, c)   ->  Path(a) / b / c")
    print("    os.path.exists(p)       ->  Path(p).exists()")
    print("    open(p).read()          ->  Path(p).read_text()")
    print("  ✅ Naye code me pathlib use karo — clean aur cross-platform")


# ==============================================================
# 3. datetime — date aur time
# ==============================================================

def datetime_demo():
    print("\n--- 3. datetime ---")

    now = datetime.now()
    today = date.today()

    print(f"  datetime.now()  = {now}")
    print(f"  date.today()    = {today}")
    print(f"  now.year/month/day = {now.year}/{now.month}/{now.day}")

    print("\n  FORMATTING (strftime — datetime se string):")
    formats = [
        ("%Y-%m-%d", "DB format"),
        ("%d/%m/%Y", "Indian format"),
        ("%d %B %Y", "Full month"),
        ("%I:%M %p", "12-hour time"),
        ("%A, %d %b %Y", "Weekday"),
    ]
    for fmt, desc in formats:
        print(f"    {fmt:<15} -> {now.strftime(fmt):<25} ({desc})")

    print("\n  PARSING (strptime — string se datetime):")
    parsed = datetime.strptime("15/01/2026", "%d/%m/%Y")
    print(f"    '15/01/2026' -> {parsed}")

    print("\n  YAAD RAKHNE KA TRICK:")
    print("    strFtime = Format  (datetime -> string)")
    print("    strPtime = Parse   (string -> datetime)")

    print("\n  timedelta (date arithmetic):")
    print(f"    Kal        = {(now + timedelta(days=1)).date()}")
    print(f"    Kal (past) = {(now - timedelta(days=1)).date()}")
    print(f"    30 din baad= {(now + timedelta(days=30)).date()}")

    print("\n  Difference nikalo:")
    joining = datetime(2026, 1, 1)
    diff = now - joining
    print(f"    Joining: {joining.date()}, aaj: {now.date()}")
    print(f"    Days:    {diff.days}")

    # Real use: age calculate
    def calculate_age(birth_date):
        t = date.today()
        return t.year - birth_date.year - (
            (t.month, t.day) < (birth_date.month, birth_date.day)
        )

    print(f"\n  calculate_age(2005-03-15) = {calculate_age(date(2005, 3, 15))} years")

    print("\n  timestamp (Unix time):")
    print(f"    now.timestamp() = {now.timestamp():.0f}")


# ==============================================================
# 4. json + csv (Step 5 ka quick recap)
# ==============================================================

def json_csv_recap():
    print("\n--- 4. json + csv (quick recap) ---")

    data = {"name": "Noman", "skills": ["Python", "SQL"], "active": True}

    print("  json:")
    print(f"    dumps -> {json.dumps(data)}")
    sample = '{"a": 1}'
    print(f"    loads -> {json.loads(sample)}")

    print("\n  csv:")
    p = OUT / "quick.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "salary"])
        w.writeheader()
        w.writerows([{"name": "Noman", "salary": 30000},
                     {"name": "Ali", "salary": 45000}])
    with open(p, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"    {len(rows)} rows -> {rows}")

    print("\n  Detail ke liye: step05_files_json.py")


# ==============================================================
# 5. re — REGULAR EXPRESSIONS (validation ka king)
# ==============================================================

def regex_demo():
    print("\n--- 5. re (REGULAR EXPRESSIONS) ---")

    print("""
  PATTERN CHEATSHEET:
    \\d   digit (0-9)          \\D   non-digit
    \\w   word char (a-z0-9_)  \\W   non-word
    \\s   whitespace           \\S   non-whitespace
    .    koi bhi char         ^    start
    $    end                  |    OR
    *    0 ya zyada           +    1 ya zyada
    ?    0 ya 1               {n}  exactly n
    {n,} n ya zyada           {n,m} n se m tak
    []   character set        ()   group (capture)
    """)

    text = "Noman ka number 9876543210 hai aur email noman@example.com hai. " \
           "Backup: 8765432109, admin@test.co.in"

    print(f"  Text: {text}\n")

    # search — pehla match
    m = re.search(r"\d{10}", text)
    print(f"  re.search(r'\\d{{10}}')  -> {m.group()} (position {m.start()})")

    # findall — saare matches
    phones = re.findall(r"[6-9]\d{9}", text)
    print(f"  re.findall(phone)     -> {phones}")

    # Email
    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
    print(f"  Emails                -> {emails}")

    # sub — replace
    masked = re.sub(r"[6-9]\d{9}", "XXXXXXXXXX", text)
    print(f"\n  re.sub (mask numbers):\n    {masked}")

    # split
    split_result = re.split(r"[,;]", "a,b;c")
    print(f"\n  re.split on 'a,b;c'   -> {split_result}")

    # ---- VALIDATION — real use case ----
    print("\n  VALIDATORS (ye interview me poochhte hain):")

    patterns = {
        "email":    r"^[\w.+-]+@[\w-]+\.[\w.]{2,}$",
        "phone_in": r"^[6-9]\d{9}$",
        "pincode":  r"^[1-9]\d{5}$",
        "pan":      r"^[A-Z]{5}\d{4}[A-Z]$",
        "password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$",
    }

    tests = [
        ("email",    ["noman@example.com", "galat-email", "a@b.co"]),
        ("phone_in", ["9876543210", "1234567890", "98765"]),
        ("pincode",  ["500001", "000001"]),
        ("pan",      ["ABCDE1234F", "abcde1234f"]),
        ("password", ["Pass@123", "weakpass", "Pass123"]),
    ]

    for key, values in tests:
        print(f"\n    {key}:")
        for v in values:
            ok = bool(re.match(patterns[key], v))
            print(f"      {'✓' if ok else '✗'}  {v}")

    # Groups
    print("\n  GROUPS (data nikalna):")
    log = "2026-01-15 ERROR Database connection failed"
    m = re.match(r"(\d{4}-\d{2}-\d{2}) (\w+) (.+)", log)
    if m:
        print(f"    Date    : {m.group(1)}")
        print(f"    Level   : {m.group(2)}")
        print(f"    Message : {m.group(3)}")

    # Named groups — zyada readable
    m = re.match(r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<level>\w+) (?P<msg>.+)", log)
    if m:
        print(f"    Named   : {m.groupdict()}")

    print("\n  match vs search vs findall:")
    print("    match()   -> SHURU se dhoondhta hai")
    print("    search()  -> KAHIN bhi pehla match")
    print("    findall() -> SAARE matches ki list")


# ==============================================================
# 6. requests — API CALLS  🔥 (Backend world ka gate)
# ==============================================================

def requests_demo():
    print("\n--- 6. requests (API CALLS) 🔥 ---")
    print("  Yahan se tu API + Backend world me enter karega.")

    code_examples = '''
  ---------------- INSTALL ----------------
  pip install requests

  ---------------- GET ----------------
  import requests

  response = requests.get("https://api.example.com/users")
  data = response.json()
  print(data)

  ---------------- STATUS CODES ----------------
  response.status_code    # 200, 404, 500...
  response.ok             # True agar < 400
  response.text           # raw string
  response.json()         # parsed dict/list
  response.headers        # response headers

  200 OK          -> sab theek
  201 Created     -> naya resource bana
  400 Bad Request -> tere data me galti
  401 Unauthorized-> login nahi hai
  403 Forbidden   -> permission nahi
  404 Not Found   -> resource nahi mila
  500 Server Error-> server ki galti

  ---------------- QUERY PARAMETERS ----------------
  response = requests.get(
      "https://api.example.com/users",
      params={"page": 2, "limit": 10}
  )
  # URL banta hai: .../users?page=2&limit=10

  ---------------- POST (data bhejna) ----------------
  response = requests.post(
      "https://api.example.com/users",
      json={"name": "Noman", "salary": 30000}
  )

  ---------------- HEADERS + AUTH (JWT) ----------------
  headers = {
      "Authorization": "Bearer YOUR_TOKEN_HERE",
      "Content-Type": "application/json",
  }
  response = requests.get(url, headers=headers)

  ---------------- PUT / PATCH / DELETE ----------------
  requests.put(url, json=full_data)      # poora replace
  requests.patch(url, json=partial)      # partial update
  requests.delete(url)                   # delete

  ---------------- TIMEOUT (HAMESHA LAGAO) ----------------
  response = requests.get(url, timeout=10)
  # Bina timeout ke program hamesha ke liye atak sakta hai

  ---------------- ERROR HANDLING (Step 4 + Step 7) ----------------
  import requests

  try:
      response = requests.get(url, timeout=10)
      response.raise_for_status()       # 4xx/5xx pe exception
      data = response.json()

  except requests.exceptions.Timeout:
      print("Request timeout ho gaya")
  except requests.exceptions.ConnectionError:
      print("Internet ya server down hai")
  except requests.exceptions.HTTPError as e:
      print(f"HTTP error: {e.response.status_code}")
  except ValueError:
      print("Response valid JSON nahi tha")

  ---------------- SESSION (performance) ----------------
  session = requests.Session()
  session.headers.update({"Authorization": "Bearer TOKEN"})
  r1 = session.get(url1)     # connection reuse hota hai
  r2 = session.get(url2)     # isliye fast

  ---------------- PRACTICE KE LIYE FREE APIs ----------------
  https://jsonplaceholder.typicode.com/users     (fake data)
  https://api.github.com/users/SyedNoman2005     (tera GitHub!)
  https://pokeapi.co/api/v2/pokemon/pikachu      (Pokemon)
  https://official-joke-api.appspot.com/random_joke
  https://api.coindesk.com/v1/bpi/currentprice.json
'''
    print(code_examples)

    # Live try karo agar requests aur internet hai
    try:
        import requests as rq
        print("  ✅ requests installed hai — live call try kar rahe hain...")
        try:
            r = rq.get("https://jsonplaceholder.typicode.com/users/1", timeout=8)
            r.raise_for_status()
            u = r.json()
            print(f"     Status  : {r.status_code}")
            print(f"     Name    : {u['name']}")
            print(f"     Email   : {u['email']}")
            print(f"     City    : {u['address']['city']}")
        except Exception as e:
            print(f"     (Network nahi hai: {type(e).__name__}) — code upar dekh lo")
    except ImportError:
        print("  ⚠️  requests installed nahi hai.")
        print("     Install karo:  pip install requests")
        print("     Phir ye script dobara chalao — live API call dikhega.")


# ==============================================================
# 7. logging — print() ka professional replacement
# ==============================================================

def logging_demo():
    print("\n--- 7. logging (print ka professional version) ---")

    log_file = OUT / "app.log"
    if log_file.exists():
        log_file.unlink()

    logger = logging.getLogger("MASTERY")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # Handler 1: file me sab kuch
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s"
    ))

    # Handler 2: console pe sirf WARNING se upar
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("    [%(levelname)s] %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)

    print("\n  5 LEVELS (kam se zyada serious):")
    print("    DEBUG    -> development ki detail")
    print("    INFO     -> normal events")
    print("    WARNING  -> kuch gadbad hai par chal raha hai")
    print("    ERROR    -> kaam fail ho gaya")
    print("    CRITICAL -> app hi mar gaya")

    print("\n  Console output (sirf WARNING+ dikhega):")
    logger.debug("Database query chalayi: SELECT * FROM employees")
    logger.info("Employee Noman add hua")
    logger.warning("Salary 10 lakh se zyada hai — verify karo")
    logger.error("Database connection fail")
    logger.critical("App crash — restart chahiye")

    print(f"\n  File me SAB kuch gaya ({log_file.name}):")
    for line in log_file.read_text(encoding="utf-8").strip().split("\n"):
        print(f"    {line}")

    print("\n  Exception ke saath (traceback automatic):")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Calculation fail hua")
        print("    (traceback file me chala gaya)")

    print("\n  print() vs logging:")
    print("    print()  -> sirf console, on/off nahi kar sakte, timestamp nahi")
    print("    logging  -> levels, file+console, timestamp, filtering, production-ready")
    print("    Django/production me HAMESHA logging use hota hai, print nahi.")


# ==============================================================
INTERVIEW = """
Q1. os vs pathlib?
    os.path -> purana, string based
    pathlib -> modern, object based, / operator, cross-platform
    Naye code me pathlib use karo.

Q2. strftime vs strptime?
    strFtime -> Format: datetime -> string
    strPtime -> Parse:  string -> datetime

Q3. timedelta kya hai?
    Time ka difference. Date arithmetic ke liye.
    now + timedelta(days=30)

Q4. re.match vs re.search vs re.findall?
    match()   -> string ke SHURU se
    search()  -> kahin bhi, pehla match
    findall() -> saare matches ki list

Q5. requests me GET vs POST?
    GET  -> data laane ke liye, params URL me
    POST -> data bhejne ke liye, body me

Q6. response.text vs response.json()?
    .text   -> raw string
    .json() -> parsed dict/list (JSON hona chahiye warna error)

Q7. raise_for_status() kya karta hai?
    4xx/5xx status pe HTTPError raise karta hai.
    Warna galat response bhi chup-chaap paas ho jaata hai.

Q8. timeout kyun zaroori hai?
    Bina timeout ke request hamesha ke liye atak sakti hai
    aur program hang ho jaayega.

Q9. print vs logging?
    logging: levels, file output, timestamps, production me on/off.
    print production code me nahi hona chahiye.

Q10. Logging ke levels?
    DEBUG < INFO < WARNING < ERROR < CRITICAL

Q11. Secrets (password, API key) kahan rakhein?
    Environment variables me (os.environ) ya .env file me.
    Code me HARDCODE kabhi nahi. .env ko gitignore karo.
"""


PRACTICE = """
1.  Current folder ki saari .py files list karo (pathlib se).
2.  Aaj ki date 3 alag formats me print karo.
3.  Apni age calculate karo date of birth se.
4.  Email validator regex likho.
5.  Indian mobile number validator (6-9 se shuru, 10 digit).
6.  Ek text se saare emails nikalo.
7.  jsonplaceholder API se users lao aur naam print karo.
8.  https://api.github.com/users/SyedNoman2005 call karo — apna data dekho.
9.  API call me poora error handling lagao (timeout, connection, http).
10. Logger banao jo file + console dono me likhe.
11. Ek script jo folder ke saare files ka size report kare.
12. CSV padh ke JSON me convert karo (csv + json saath me).
"""


if __name__ == "__main__":
    print("=" * 62)
    print("STEP 7 — USEFUL LIBRARIES")
    print("=" * 62)

    os_demo()
    pathlib_demo()
    datetime_demo()
    json_csv_recap()
    regex_demo()
    requests_demo()
    logging_demo()

    print("\n" + "=" * 62)
    print("INTERVIEW QUESTIONS")
    print("=" * 62)
    print(INTERVIEW)

    print("=" * 62)
    print("PRACTICE")
    print("=" * 62)
    print(PRACTICE)
