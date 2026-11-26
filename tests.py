import gc
from pathlib import Path
import tempfile

import logic
import storage


def run_tests() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "test.db"
        storage.init(db)

        item1 = storage.add("TVA-01", "alpha", 4.5, "first", db_path=db)
        item2 = storage.add("TVA-02", "beta", 2.0, "second", db_path=db)
        assert item1["code"] == "TVA-01"
        assert item2["branch"] == "beta"

        all_items = storage.load(db_path=db)
        assert len(all_items) == 2

        alpha_items = storage.load(branch="alpha", db_path=db)
        assert len(alpha_items) == 1
        assert alpha_items[0]["code"] == "TVA-01"

        found = logic.find_by_branch(all_items, "beta")
        assert len(found) == 1
        assert found[0]["code"] == "TVA-02"

        summary = logic.summarize_records(all_items)
        report_text = logic.format_report(summary)
        assert isinstance(report_text, str) and len(report_text) > 0

        assert storage.delete(item1["id"], db_path=db) is True
        assert storage.delete(999999, db_path=db) is False
        assert len(storage.load(db_path=db)) == 1

        gc.collect()

    print("OK: tests.py passed")


if __name__ == "__main__":
    run_tests()
