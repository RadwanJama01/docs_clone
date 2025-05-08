# app/routes/users.py

from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db

user_bp = Blueprint("users", __name__)  # <- MATCH THIS NAME

@user_bp.route('/user/profile', methods=["GET"])
def user_profile():
    user = User.query.first()
    if not user:
        return jsonify({"message": "No User Found"}), 404
    return jsonify({"username": user.username, "email": user.email})

@user_bp.route('/user/all', methods=["GET"])
def all_users():
    try:
        users = User.query.all()
        user_list = [{"username": user.username, "email": user.email} for user in users]
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

