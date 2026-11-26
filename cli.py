import sys
from logic import format_report, summarize_records
from storage import add_record, load_records


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args or args[0] in ("-h", "--help", "help"):
        print("Використання:")
        print("  python cli.py add <КОД> <ГІЛКА> <РИЗИК> <ПРИМІТКА>")
        print("  python cli.py list")
        print("  python cli.py report")
        return 0

    cmd = args[0]
    if cmd == "add":
        if len(args) < 5:
            print("Помилка: потрібно передати <КОД> <ГІЛКА> <РИЗИК> <ПРИМІТКА>")
            return 1
        code, branch, risk_str, note = args[1], args[2], args[3], " ".join(args[4:])
        try:
            risk = float(risk_str)
        except ValueError:
            print("Помилка: ризик має бути числом (наприклад, 15.5)")
            return 1
        rec = add_record(code, branch, risk, note)
        print(f"Додано запис: [{rec['code']}] гілка={rec['branch']} ризик={rec['risk']} — {rec['note']}")
        return 0

    if cmd == "list":
        records = load_records()
        if not records:
            print("Архів TVA порожній.")
            return 0
        for r in records:
            print(f"[{r['code']}] Гілка: {r['branch']} | Ризик: {r['risk']} | {r['note']}")
        return 0

    if cmd == "report":
        records = load_records()
        summary = summarize_records(records)
        print(format_report(summary))
        return 0

    print(f"Невідома команда: {cmd}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
