# Merge it with CLI (Beginner Copy/Paste)

Below is the exact command-line flow you asked for:

- Create `test-branch` from `main`
- Add new Python code in another branch
- Merge that code into `test-branch`

---

## 1) Connect GitHub CLI

```bash
gh auth login
gh auth status
```

---

## 2) Create `test-branch` from `main`

```bash
git checkout main
git pull origin main
git checkout -b test-branch
git push -u origin test-branch
```

---

## 3) Create a feature branch from `test-branch`

```bash
git checkout test-branch
git pull origin test-branch
git checkout -b feature/python-new-code
```

---

## 4) Add Python code in that feature branch

```bash
cat > app.py <<'PY'
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    print(add(2, 3))
PY

python3 app.py
```

Commit and push:

```bash
git add app.py
git commit -m "Add new Python code example"
git push -u origin feature/python-new-code
```

---

## 5) Merge feature into `test-branch` (GitHub CLI way)

Create PR to `test-branch`:

```bash
gh pr create \
  --base test-branch \
  --head feature/python-new-code \
  --title "Add Python code" \
  --body "Adds app.py with a simple function"
```

Merge it:

```bash
gh pr merge --merge --delete-branch
```

---

## 6) Alternative: merge locally with Git (no PR)

```bash
git checkout test-branch
git pull origin test-branch
git merge feature/python-new-code
git push origin test-branch
```

---

## Fast version (all key commands)

```bash
gh auth login && gh auth status

git checkout main && git pull origin main
git checkout -b test-branch && git push -u origin test-branch

git checkout -b feature/python-new-code

echo 'print("hello from python")' > app.py
git add app.py && git commit -m "Add Python code" && git push -u origin feature/python-new-code

gh pr create --base test-branch --head feature/python-new-code --title "Add Python code" --body "Adds app.py"
gh pr merge --merge --delete-branch
```
