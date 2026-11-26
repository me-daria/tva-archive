from flask import Flask, request, jsonify
from flask_cors import CORS
import storage
import logic

app = Flask(__name__)
CORS(app, origins=["https://tva-archive.pp.ua"])
storage.init()


@app.get("/items")
def list_items():
    branch = request.args.get("branch")
    return jsonify(storage.load(branch))


@app.post("/items")
def add_item():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "очікується JSON-об'єкт"}), 400

    for field in ("code", "branch", "risk"):
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"error": f"немає або порожнє поле {field}"}), 400

    try:
        risk = float(data["risk"])
    except (ValueError, TypeError):
        return jsonify({"error": "risk має бути числом"}), 400

    note = str(data.get("note", ""))
    created = storage.add(data["code"], data["branch"], risk, note)
    return jsonify(created), 201


@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    if storage.delete(item_id):
        return jsonify({"deleted": item_id}), 200
    return jsonify({"error": "не знайдено"}), 404


@app.get("/report")
def report():
    items = storage.load()
    if hasattr(logic, "report_by_branch"):
        return jsonify(logic.report_by_branch(items)), 200
    if hasattr(logic, "total_by_branch"):
        return jsonify(logic.total_by_branch(items)), 200
    totals = {}
    for item in items:
        b = item["branch"]
        totals[b] = totals.get(b, 0.0) + item["risk"]
    return jsonify(totals), 200


if __name__ == "__main__":
    app.run(debug=True)