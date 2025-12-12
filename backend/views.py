from flask import jsonify, request, abort
from backend import app
from datetime import datetime

users = []
categories = []
records = []

user_id_counter = 1
category_id_counter = 1
record_id_counter = 1


@app.route("/healthcheck")
def healthcheck():
    return {"status": "OK", "message": "Backend is functional"}


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    abort(404, description="User not found")


@app.route("/user", methods=["POST"])
def create_user():
    global user_id_counter
    data = request.get_json()

    if not data or "name" not in data:
        abort(400, description="Name is required")

    new_user = {
        "id": user_id_counter,
        "name": data["name"]
    }
    users.append(new_user)
    user_id_counter += 1
    return jsonify(new_user)


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        abort(404, description="User not found")

    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted"})


@app.route("/category", methods=["GET"])
def get_categories():
    return jsonify(categories)


@app.route("/category", methods=["POST"])
def create_category():
    global category_id_counter
    data = request.get_json()

    if not data or "name" not in data:
        abort(400, description="Category name is required")

    new_category = {
        "id": category_id_counter,
        "name": data["name"]
    }
    categories.append(new_category)
    category_id_counter += 1
    return jsonify(new_category)


@app.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    global categories
    category = next((c for c in categories if c["id"] == category_id), None)
    if not category:
        abort(404, description="Category not found")

    categories = [c for c in categories if c["id"] != category_id]
    return jsonify({"message": "Category deleted"})


@app.route("/record", methods=["POST"])
def create_record():
    global record_id_counter
    data = request.get_json()

    if not data or "user_id" not in data or "category_id" not in data or "amount" not in data:
        abort(400, description="Missing required fields")

    user_exists = any(u["id"] == data["user_id"] for u in users)
    category_exists = any(c["id"] == data["category_id"] for c in categories)

    if not user_exists:
        abort(400, description="User does not exist")
    if not category_exists:
        abort(400, description="Category does not exist")

    new_record = {
        "id": record_id_counter,
        "user_id": data["user_id"],
        "category_id": data["category_id"],
        "timestamp": datetime.now().isoformat(),
        "amount": data["amount"]
    }
    records.append(new_record)
    record_id_counter += 1
    return jsonify(new_record)


@app.route("/record/<int:record_id>", methods=["GET"])
def get_record(record_id):
    record = next((r for r in records if r["id"] == record_id), None)
    if record:
        return jsonify(record)
    abort(404, description="Record not found")


@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    global records
    record = next((r for r in records if r["id"] == record_id), None)
    if not record:
        abort(404, description="Record not found")

    records = [r for r in records if r["id"] != record_id]
    return jsonify({"message": "Record deleted"})


@app.route("/record", methods=["GET"])
def get_records_filtered():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")

    if not user_id and not category_id:
        abort(400, description="Filter parameters (user_id or category_id) are required")

    filtered_records = records

    if user_id:
        filtered_records = [r for r in filtered_records if r["user_id"] == int(user_id)]

    if category_id:
        filtered_records = [r for r in filtered_records if r["category_id"] == int(category_id)]

    return jsonify(filtered_records)