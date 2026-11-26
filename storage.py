from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data.txt"


def load_records(path: Path = DATA_FILE) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) != 4:
            continue
        code, branch, risk_str, note = parts
        try:
            risk = float(risk_str)
        except ValueError:
            continue
        records.append({
            "code": code.strip(),
            "branch": branch.strip(),
            "risk": risk,
            "note": note.strip(),
        })
    return records


def save_records(records: list[dict], path: Path = DATA_FILE) -> None:
    lines = [
        f"{r['code']}|{r['branch']}|{r['risk']}|{r['note']}"
        for r in records
    ]
    content = "\n".join(lines) + ("\n" if lines else "")
    path.write_text(content, encoding="utf-8")


def add_record(code: str, branch: str, risk: float, note: str, path: Path = DATA_FILE) -> dict:
    records = load_records(path)
    new_rec = {
        "code": code.strip(),
        "branch": branch.strip(),
        "risk": float(risk),
        "note": note.strip(),
    }
    records.append(new_rec)
    save_records(records, path)
    return new_rec
