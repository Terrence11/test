from pathlib import Path
import shutil
root = Path(__file__).resolve().parent
current = root / "data" / "eval_questions.jsonl"
replacement = root / "data" / "eval_questions_hard.jsonl"
if not replacement.exists():
    raise SystemExit("Missing data/eval_questions_hard.jsonl: copy files into rag_week_full first")
if current.exists():
    backup = root / "data" / "eval_questions_before_hard.jsonl"
    if not backup.exists():
        shutil.copy2(current, backup)
        print(f"Backup: {backup}")
shutil.copy2(replacement, current)
print(f"Activated {sum(bool(x.strip()) for x in current.read_text().splitlines())} hard evaluation questions")
