# backend/app/routes/main.py
from flask import Blueprint, jsonify, request, render_template, abort
from app.extensions import db
from app.models.user import User

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("base.html")

@main_bp.route("/health")
def health():
    return jsonify({"status": "ok"})

# CRUD para User
@main_bp.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@main_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@main_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@main_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400
    user.name = name
    db.session.commit()
    return jsonify(user.to_dict())

@main_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"deleted": user_id})
