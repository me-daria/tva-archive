from pathlib import Path
from logic import format_report, summarize_records
from storage import add_record, load_records, save_records


def run_tests() -> None:
    test_file = Path(__file__).resolve().parent / "test_temp_data.txt"
    if test_file.exists():
        test_file.unlink()

    assert load_records(test_file) == []

    add_record("TL-101", "Alpha", 12.5, "варіант Локі", path=test_file)
    add_record("TL-102", "Beta", 27.5, "відхилення лінії часу", path=test_file)

    loaded = load_records(test_file)
    assert len(loaded) == 2
    assert loaded[0]["code"] == "TL-101"
    assert loaded[1]["risk"] == 27.5

    summary = summarize_records(loaded)
    assert summary["total"] == 2
    assert summary["avg_risk"] == 20.0
    assert summary["max_risk"] == 27.5
    assert summary["by_branch"] == {"Alpha": 1, "Beta": 1}

    report = format_report(summary)
    assert "Усього аномалій: 2" in report
    assert "Середній ризик: 20.0" in report

    save_records([], test_file)
    assert load_records(test_file) == []

    if test_file.exists():
        test_file.unlink()

    print("УСІ ТЕСТИ ПРОЙШЛИ")


if __name__ == "__main__":
    run_tests()
