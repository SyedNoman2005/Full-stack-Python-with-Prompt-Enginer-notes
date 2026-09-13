# STEP 8 — pip + VIRTUAL ENVIRONMENT 🔴

Ye real projects ke liye hai. Django start karne se pehle ye aana **must** hai.

---

## Problem Kya Hai?

Do projects hain:
- Project A → Django 3.2 chahiye
- Project B → Django 5.0 chahiye

Ek hi system me dono kaise? **Virtual Environment se.**

Har project ka apna alag Python + apni alag libraries. Ek project ki library doosre ko touch nahi karti.

---

## venv Banao

```bash
# Folder me jao
cd my_project

# venv banao
python -m venv venv

# Linux / Mac pe:
python3 -m venv venv
```

Ab ek `venv/` folder ban gaya. Isme Python ki copy aur libraries jaayengi.

---

## Activate Karo

**Windows (CMD):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```
> Error aaye to ek baar ye chalao:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Linux / Mac:**
```bash
source venv/bin/activate
```

**Activate hua ya nahi?** Terminal me aage `(venv)` dikhega:
```
(venv) C:\my_project>
```

**Deactivate:**
```bash
deactivate
```

---

## pip — Package Manager

```bash
pip install requests                  # install
pip install django==5.0               # specific version
pip install "django>=4.2,<5.0"        # version range
pip install --upgrade requests        # upgrade
pip uninstall requests                # remove

pip list                              # sab installed packages
pip show django                       # ek package ki detail
pip freeze                            # exact versions (requirements ke liye)
```

---

## requirements.txt — Bahut Important

Ye file batati hai ki project ko kaun si libraries chahiye.

**Banao:**
```bash
pip freeze > requirements.txt
```

**File aisi dikhti hai:**
```
asgiref==3.8.1
Django==5.0.6
djangorestframework==3.15.1
mysql-connector-python==8.4.0
requests==2.32.3
sqlparse==0.5.0
```

**Kisi aur ke system pe install:**
```bash
pip install -r requirements.txt
```

> **Interview me poochha jaata hai:** "requirements.txt kya hai?"
> Jawab: Project ki dependencies ki list with exact versions. Isse koi bhi developer same environment bana sakta hai.

---

## Complete Workflow — Naya Project

```bash
# 1. Folder banao
mkdir my_django_project
cd my_django_project

# 2. venv banao
python -m venv venv

# 3. Activate
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# 4. Libraries install
pip install django djangorestframework mysql-connector-python

# 5. requirements save
pip freeze > requirements.txt

# 6. Kaam karo
django-admin startproject config .

# 7. Git
git init
echo "venv/" > .gitignore       # venv KABHI commit mat karna
git add .
git commit -m "Initial setup"
```

---

## ⚠️ venv Kabhi Git Me Commit Mat Karna

`.gitignore` me ye zaroor daalo:

```gitignore
venv/
env/
.venv/
__pycache__/
*.pyc
.env
db.sqlite3
```

**Kyun?**
- venv me hazaron files hoti hain (100+ MB)
- Har system ke liye alag hoti hai
- `requirements.txt` kaafi hai — usse koi bhi dobara bana lega

---

## Common Errors

| Error | Solution |
|---|---|
| `'python' is not recognized` | Python PATH me nahi hai. Reinstall karo "Add to PATH" tick karke |
| `cannot be loaded because running scripts is disabled` | PowerShell: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `pip is not recognized` | `python -m pip install ...` use karo |
| Package install hua par import nahi ho raha | venv activate nahi hai. `(venv)` check karo |
| `ModuleNotFoundError` after activate | Galat venv activate hai. Deactivate karke sahi wala karo |

---

## Interview Questions

**Q1. Virtual environment kya hai aur kyun chahiye?**
Isolated Python environment. Har project ki apni libraries, apne versions. Version conflicts nahi hote.

**Q2. venv kaise banate hain?**
`python -m venv venv`, phir activate karo.

**Q3. requirements.txt kya hai?**
Project ki dependencies ki list exact versions ke saath. `pip freeze > requirements.txt` se banti hai, `pip install -r requirements.txt` se install hoti hai.

**Q4. `pip list` vs `pip freeze`?**
`pip list` — readable table format
`pip freeze` — `package==version` format, requirements.txt ke liye

**Q5. venv ko git me commit karna chahiye?**
Bilkul nahi. `.gitignore` me daalo. `requirements.txt` commit karo.

**Q6. venv vs virtualenv vs conda?**
`venv` — Python 3 me built-in, standard choice
`virtualenv` — third-party, thoda fast, Python 2 support
`conda` — data science ke liye, non-Python packages bhi handle karta hai

---

## Practice

1. Naya folder banao aur usme venv banao
2. Activate karo aur `(venv)` dekho
3. `pip install requests` karo
4. `pip list` se check karo
5. `requirements.txt` banao
6. venv delete karo, dobara banao, `pip install -r requirements.txt` se restore karo
7. `.gitignore` banao venv ke saath
