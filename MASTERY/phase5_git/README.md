# 🐙 PHASE 5 — GIT & GITHUB

Sirf commands ratne se kuch nahi hoga. **Real workflow** practice karo.

---

## Ek Baar Ka Setup

```bash
git config --global user.name "SyedNoman2005"
git config --global user.email "tera_github_email@example.com"

# Check
git config --list
```

---

## STEP 18 — Basic Commands 🔴🔴

### Git Ke 4 Area (Ye Diagram Samajh Lo)

```
  WORKING DIRECTORY          STAGING AREA           LOCAL REPO          REMOTE (GitHub)
  (tere files)               (ready to commit)      (commits)           (cloud)
        │                          │                     │                   │
        │──── git add ────────────▶│                     │                   │
        │                          │──── git commit ────▶│                   │
        │                          │                     │──── git push ────▶│
        │◀───────────────── git pull / git clone ────────────────────────────│
```

### Commands

```bash
git init                    # naya repo shuru karo
git status                  # kya badla hai? (SABSE ZYADA USE HOGA)
git add filename.py         # ek file stage karo
git add .                   # sab stage karo
git commit -m "message"     # snapshot banao
git log                     # history dekho
git log --oneline           # chhoti history
git log --oneline --graph   # branch graph ke saath
git diff                    # kya badla (unstaged)
git diff --staged           # kya badla (staged)
git show HEAD               # last commit ki detail
```

### Remote (GitHub) Ke Saath

```bash
git clone https://github.com/user/repo.git    # copy download
git remote -v                                 # remote URLs dekho
git remote add origin <url>                   # remote jodo
git push origin main                          # upload
git pull origin main                          # download + merge
git fetch                                     # download (merge nahi)
```

### Undo Commands (Bachaate Hain)

```bash
git restore file.py                  # file ke changes wapas
git restore --staged file.py         # unstage karo (add undo)
git commit --amend -m "naya msg"     # last commit ka message badlo
git reset --soft HEAD~1              # commit undo, changes bache
git reset --hard HEAD~1              # commit undo, changes GAYAB ⚠️
git revert <commit-hash>             # ulta commit banao (safe)
git stash                            # changes side me rakho
git stash pop                        # wapas lao
```

> **`reset --hard` se dhyan** — kaam hamesha ke liye ja sakta hai. Public branch pe `revert` use karo.

---

## STEP 19 — Branching

```bash
git branch                      # saari branches
git branch feature-login        # nayi branch banao
git switch feature-login        # switch karo (modern)
git checkout feature-login      # switch karo (purana)
git switch -c feature-login     # bana ke switch — 2 in 1

git merge feature-login         # is branch me merge karo
git branch -d feature-login     # delete (merge ho chuki)
git branch -D feature-login     # force delete
git push origin --delete feature-login   # remote se delete
```

### Kyun Branch?

`main` hamesha **working** rehni chahiye. Naya feature alag branch me banao, test karo, phir merge.

---

## Real Workflow (Ye Practice Karo)

```
GitHub Repository
      ↓  git clone
  Local Copy
      ↓  git switch -c feature-x
  Nayi Branch
      ↓  code likho
  Changes
      ↓  git add .
  Staged
      ↓  git commit -m "feat: add x"
  Committed
      ↓  git push origin feature-x
  GitHub pe branch
      ↓  Pull Request banao
  Review
      ↓  Merge
  main updated
```

**Complete example:**
```bash
git clone https://github.com/SyedNoman2005/my-project.git
cd my-project

git switch -c feature-search
# ... code likho ...
git status
git add .
git commit -m "feat: add employee search with filters"
git push origin feature-search

# GitHub pe jao -> "Compare & pull request" -> Create PR -> Merge

git switch main
git pull origin main
git branch -d feature-search
```

---

## Merge Conflict Kaise Handle Karein

Jab do log same line badal dein:

```
<<<<<<< HEAD
salary = 30000          # teri line
=======
salary = 35000          # unki line
>>>>>>> feature-branch
```

**Fix:**
1. File kholo
2. Decide karo kaunsa code rakhna hai
3. `<<<<<<<`, `=======`, `>>>>>>>` markers **hata do**
4. `git add file.py`
5. `git commit`

```bash
git merge --abort        # merge cancel karna ho to
```

---

## .gitignore — Zaroor Banao

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
env/
.venv/

# Environment / Secrets
.env
*.key
config_local.py

# Database
*.db
*.sqlite3

# Node
node_modules/
dist/
build/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

**⚠️ Kabhi commit mat karna:** passwords, API keys, `.env`, `venv/`, `node_modules/`, database files.

> Galti se password push ho gaya? Use **turant rotate** karo. Git history se hatana mushkil hai — value badal do.

---

## Commit Message Kaise Likhein

**❌ Kharab:**
```
update
fix
asdfgh
changes
```

**✅ Achha (Conventional Commits):**
```
feat: add employee search with department filter
fix: handle NULL salary in statistics report
docs: update README with setup steps
refactor: extract validation into separate module
test: add SQL injection tests for search
chore: update requirements.txt
```

**Format:** `type: kya kiya (present tense, chhota)`

Recruiters tera commit history dekhte hain. Achhe messages = professional lagta hai.

---

## Interview Questions

**Q1. Git vs GitHub?**
Git — distributed version control software, tere system pe install hota hai.
GitHub — cloud platform jahan Git repos host hote hain + collaboration features.

**Q2. `git fetch` vs `git pull`?**
`fetch` — remote se changes download, merge nahi.
`pull` = `fetch` + `merge`.

**Q3. `git merge` vs `git rebase`?**
`merge` — merge commit banata hai, history branched rehti hai (safe).
`rebase` — commits ko upar rakh deta hai, history linear (saaf, par history rewrite karta hai).
**Rule:** shared/public branch pe kabhi rebase mat karo.

**Q4. `git reset` vs `git revert`?**
`reset` — history se commit hatata hai (private branch pe)
`revert` — ulta commit banata hai (public branch pe — safe)

**Q5. Staging area kya hai?**
Working directory aur commit ke beech ka buffer. Yahan decide karte ho ki kaunse changes commit karne hain.

**Q6. HEAD kya hai?**
Current branch ke latest commit ka pointer.

**Q7. Merge conflict kab hota hai?**
Jab do branches me same file ki same line badli ho. Manually resolve karna padta hai.

**Q8. Pull Request kya hai?**
GitHub ka feature — code review ke liye request. Merge se pehle team review karti hai.

**Q9. `git stash` kya karta hai?**
Incomplete changes temporarily side me rakh deta hai, taaki branch switch kar sako.

**Q10. Fork vs Clone?**
Fork — GitHub pe apni copy banana (open source contribution ke liye)
Clone — repo ko apne system pe download karna

---

## Practice (Ye Sab Karo)

1. Local repo banao, 3 commits karo
2. `git log --oneline --graph` se history dekho
3. GitHub pe repo banao aur push karo
4. `feature-x` branch banao, change karo, merge karo
5. **Jaan bujh ke merge conflict banao** aur solve karo
6. `.gitignore` banao aur test karo (ek `.env` file bana ke dekho ki ignore hoti hai)
7. **Khud ka Pull Request banao aur merge karo**
8. `git stash` / `git stash pop` try karo
9. `git revert` se ek commit undo karo
10. Kisi open source repo ko fork karo aur PR bhejo

---

## Tera Actual Task

Ye `MASTERY/` folder hi tera pehla proper Git project hai:

```bash
cd /path/to/Full-stack-Python-with-Prompt-Enginer-notes

git status
git add MASTERY/
git commit -m "feat: add Python + SQL mastery track with EMS project"
git push origin arena/01a09581-full-stack-python-with-prompt
```

**Roz commit kar.** GitHub contribution graph green rakhna — recruiters wahi dekhte hain.
