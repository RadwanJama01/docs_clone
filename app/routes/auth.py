from flask import Blueprint, request,jsonify
from app.models.user import User
from app import db


auth_bp = Blueprint('auth', __name__)
# Route to add a new user
@auth_bp.route('/user/add', methods=["POST"])
def add_user():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")  # You should request password here as well
    
    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"}), 400
    
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists in the database"}), 409
    
    new_user = User(username=username, email=email)
    new_user.setPassword(password)  # Set the hashed password using the setPassword method
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(f"ERRORRR AS {e}")
        return jsonify({"message": "Couldn't go through error 5000!!"}), 500
    
    return jsonify({"message": "User added successfully!"}), 201


# Route to login (username and password)
@auth_bp.route('/user/login', methods=["POST"])
def user_login():
    data = request.get_json()
    password = data.get('password')
    email = data.get('email')
    
    if not password or not email:
        return jsonify({"message": "Email and password required!"}), 400
    
    user = User.query.filter_by(email=email).first()  # Fetch user by email
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if not user.check_password(password):  # Validate password
        return jsonify({"message": "Incorrect password"}), 401
    
    return jsonify({"message": "Login successful", "username": user.username}), 200
