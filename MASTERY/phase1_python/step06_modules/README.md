# STEP 6 — MODULES + PACKAGES 🟡

Chalane ke liye:
```bash
python3 phase1_python/step06_modules/main.py
```

Deep theory ki zarurat nahi. Bas practical level.

## Folder Structure

```
step06_modules/
├── README.md
├── main.py                 <- yahan se chalao
├── calculator.py           <- simple MODULE
└── employee_package/       <- PACKAGE (folder with __init__.py)
    ├── __init__.py
    ├── models.py
    └── utils.py
```

## Module vs Package

| | Module | Package |
|---|---|---|
| Kya hai | Ek `.py` file | Folder with `__init__.py` |
| Example | `calculator.py` | `employee_package/` |
| Import | `import calculator` | `from employee_package import models` |

## Import Ke Tareeke

```python
import calculator                      # poora module
calculator.add(2, 3)

from calculator import add             # sirf ek function
add(2, 3)

from calculator import add, subtract   # kai functions
import calculator as calc              # ALIAS
from calculator import add as plus     # function alias
from calculator import *               # SAB — ye MAT karo (naam clash hote hain)
```

## `__name__ == "__main__"` — Ye Zaroor Samajh

Har Python file me ek chhupa hua variable hota hai `__name__`.

- File **directly chalao** → `__name__` = `"__main__"`
- File **import karo** → `__name__` = `"calculator"` (file ka naam)

```python
if __name__ == "__main__":
    # Ye tabhi chalega jab file DIRECTLY chalao
    # Import karne pe NAHI chalega
    print("Testing...")
```

**Kyun zaroori hai?** Bina iske, jab tu module import karega to uska saara test code bhi chal padega. Har professional Python file me ye line hoti hai.

## Interview Questions

**Q1. Module kya hai?**
Ek `.py` file jisme functions/classes/variables hote hain. Code organize karne ke liye.

**Q2. Package kya hai?**
Modules ka folder. `__init__.py` file honi chahiye (Python 3.3+ me optional, par likhna best practice hai).

**Q3. `__init__.py` ka kaam?**
Python ko batata hai ki ye folder ek package hai. Package-level imports bhi define kar sakte ho.

**Q4. `import *` kyun bura hai?**
- Pata nahi chalta kya import hua
- Naam clash ho sakte hain
- Editor auto-complete kaam nahi karta

**Q5. `__name__ == "__main__"` kyun likhte hain?**
Taaki file import hone pe test/demo code na chale, sirf direct run pe chale.

**Q6. Python module kahan dhoondhta hai?**
`sys.path` me — current directory → PYTHONPATH → site-packages.

## Practice

1. `calculator.py` module banao — add, subtract, multiply, divide
2. `main.py` se import karke use karo
3. Alias use karke import karo
4. Ek package banao 2 modules ke saath
5. `__init__.py` me kuch import karo aur package level pe expose karo
6. `if __name__ == "__main__"` add karo aur test karo ki import pe kya hota hai
