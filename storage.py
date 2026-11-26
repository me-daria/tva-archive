from pathlib import Path
import sqlite3

DB_FILE = Path(__file__).resolve().parent / "data.db"


def connect(db_path: Path = DB_FILE) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init(db_path: Path = DB_FILE) -> None:
    """Створює таблицю items, якщо її ще немає."""
    with connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                branch TEXT NOT NULL,
                risk REAL NOT NULL,
                note TEXT
            )
            """
        )


def load(branch: str | None = None, db_path: Path = DB_FILE) -> list[dict]:
    """Повертає список записів у вигляді словників (за бажанням фільтр за branch)."""
    init(db_path)
    with connect(db_path) as conn:
        if branch:
            rows = conn.execute(
                "SELECT id, code, branch, risk, note FROM items WHERE branch = ? ORDER BY id",
                (branch.strip(),),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, code, branch, risk, note FROM items ORDER BY id"
            ).fetchall()
    return [dict(row) for row in rows]


def add(code: str, branch: str, risk: float, note: str = "", db_path: Path = DB_FILE) -> dict:
    """Додає запис у базу і повертає створений словник з id."""
    init(db_path)
    clean_code = code.strip()
    clean_branch = branch.strip()
    clean_risk = float(risk)
    clean_note = note.strip()
    with connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO items (code, branch, risk, note) VALUES (?, ?, ?, ?)",
            (clean_code, clean_branch, clean_risk, clean_note),
        )
        new_id = cur.lastrowid
    return {
        "id": new_id,
        "code": clean_code,
        "branch": clean_branch,
        "risk": clean_risk,
        "note": clean_note,
    }


def delete(item_id: int, db_path: Path = DB_FILE) -> bool:
    """Видаляє запис за id. Повертає True, якщо запис існував."""
    init(db_path)
    with connect(db_path) as conn:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        return cur.rowcount > 0
