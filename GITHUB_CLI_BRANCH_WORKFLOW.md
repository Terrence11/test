# GitHub CLI + Git Branch Workflow (Beginner Example)

This guide shows a simple command-line flow to:

1. Authenticate with GitHub.
2. Create a branch from `main` (example branch: `test-branch`).
3. Create new Python code in that branch.
4. Merge your code into `test-branch` (with a feature branch example).

---

## 1) Connect your local machine to GitHub

```bash
gh auth login
```

Typical prompts:
- **GitHub.com**
- **HTTPS**
- **Login with a web browser** (or token)

Check auth status:

```bash
gh auth status
```

---

## 2) Make sure your local `main` is up to date

```bash
git checkout main
git pull origin main
```

---

## 3) Create `test-branch` from `main`

```bash
git checkout -b test-branch
```

Publish the new branch to GitHub:

```bash
git push -u origin test-branch
```

---

## 4) (Recommended) Create a feature branch from `test-branch`

This keeps your work clean and makes code review easier.

```bash
git checkout test-branch
git pull origin test-branch
git checkout -b feature/add-python-code
```

---

## 5) Add new Python code in your feature branch

Example file creation:

```bash
cat > hello_feature.py <<'PY'
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("GitHub"))
PY
```

Run it:

```bash
python3 hello_feature.py
```

Commit your change:

```bash
git add hello_feature.py
git commit -m "Add greeting example in Python"
git push -u origin feature/add-python-code
```

---

## 6) Merge feature branch into `test-branch`

### Option A: GitHub Pull Request (best practice)

Create PR targeting `test-branch`:

```bash
gh pr create \
  --base test-branch \
  --head feature/add-python-code \
  --title "Add new Python greeting example" \
  --body "Adds hello_feature.py with a simple greet function."
```

Merge PR from CLI:

```bash
gh pr merge --merge --delete-branch
```

### Option B: Local merge (quick/manual)

```bash
git checkout test-branch
git pull origin test-branch
git merge feature/add-python-code
git push origin test-branch
```

---

## 7) Verify branch history

```bash
git log --oneline --graph --decorate --all -n 15
```

---

## Quick one-line flow (reference)

```bash
git checkout main && git pull origin main && git checkout -b test-branch && git push -u origin test-branch
```

Then create feature branch + code + PR:

```bash
git checkout -b feature/add-python-code \
&& echo 'print("hello")' > hello_feature.py \
&& git add hello_feature.py \
&& git commit -m "Add hello_feature.py" \
&& git push -u origin feature/add-python-code
```
