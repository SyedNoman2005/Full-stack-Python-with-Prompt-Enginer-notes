"""
================================================================
EMS — CONFIG
================================================================
Database switch karne ke liye SIRF ye ek variable badalna hai.

  DB_TYPE = "sqlite"   -> practice ke liye (zero setup)  [DEFAULT]
  DB_TYPE = "mysql"    -> MySQL install karne ke baad

MySQL use karna ho to:
  1. Neeche DB_TYPE = "mysql" kar do
  2. MYSQL_CONFIG me apna password daalo
  3. pip install mysql-connector-python
  4. phase3_database/schema_mysql.sql chala lo
================================================================
"""

import os
from pathlib import Path

# ----------------------------------------------------------------
# YAHAN BADLO
# ----------------------------------------------------------------
DB_TYPE = os.environ.get("EMS_DB_TYPE", "sqlite")     # "sqlite" ya "mysql"


# ----------------------------------------------------------------
# SQLite settings
# ----------------------------------------------------------------
SQLITE_PATH = Path(__file__).parent / "ems.db"


# ----------------------------------------------------------------
# MySQL settings
# ----------------------------------------------------------------
# ⚠️ Password code me hardcode karna BAD PRACTICE hai.
#    Real project me environment variable use karo — jaise neeche kiya hai.
MYSQL_CONFIG = {
    "host":     os.environ.get("MYSQL_HOST", "localhost"),
    "user":     os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "your_password_here"),
    "database": os.environ.get("MYSQL_DATABASE", "ems_db"),
    "port":     int(os.environ.get("MYSQL_PORT", 3306)),
}


# ----------------------------------------------------------------
# PLACEHOLDER — yahi sabse bada syntax fark hai
#   SQLite -> ?
#   MySQL  -> %s
# ----------------------------------------------------------------
PLACEHOLDER = "?" if DB_TYPE == "sqlite" else "%s"


def q(sql: str) -> str:
    """
    Query me '?' ko sahi placeholder me badal do.

    Hum saari queries '?' ke saath likhte hain.
    MySQL pe chalti hai to ye function '%s' bana deta hai.
    Isse ek hi code dono DB pe chalta hai.
    """
    if PLACEHOLDER == "?":
        return sql
    return sql.replace("?", "%s")


# ----------------------------------------------------------------
# App settings
# ----------------------------------------------------------------
APP_NAME = "Employee Management System"
APP_VERSION = "1.0.0"
PAGE_SIZE = 10
