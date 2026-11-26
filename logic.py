def find_by_branch(records: list[dict], branch_query: str) -> list[dict]:
    needle = branch_query.strip().lower()
    if not needle:
        return []
    return [r for r in records if needle in str(r.get("branch", "")).lower()]


def summarize_records(records: list[dict]) -> dict:
    total = len(records)
    if total == 0:
        return {
            "total": 0,
            "avg_risk": 0.0,
            "max_risk": 0.0,
            "by_branch": {},
        }
    risks = [float(r["risk"]) for r in records]
    by_branch: dict[str, int] = {}
    for r in records:
        b = str(r["branch"])
        by_branch[b] = by_branch.get(b, 0) + 1
    return {
        "total": total,
        "avg_risk": round(sum(risks) / total, 2),
        "max_risk": max(risks),
        "by_branch": by_branch,
    }


def format_report(summary: dict) -> str:
    lines = [
        "=== ЗВІТ АРХІВУ TVA ===",
        f"Усього аномалій: {summary['total']}",
        f"Середній ризик: {summary['avg_risk']}",
        f"Максимальний ризик: {summary['max_risk']}",
        "За гілками часу:",
    ]
    by_branch = summary.get("by_branch", {})
    if not by_branch:
        lines.append("  (немає даних)")
    else:
        for branch, count in sorted(by_branch.items()):
            lines.append(f"  - {branch}: {count}")
    return "\n".join(lines)
