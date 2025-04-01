from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configuring database URI and other settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/rjama/flask-backend/instance/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration manager
db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)  # ✅ NO unique=True


    def setPassword(self, password):
        # This function hashes the password before storing it
        self.passwordHash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)


    def check_password(self, password):
        # This function checks if the provided password matches the hash
        return check_password_hash(self.passwordHash, password)

    def __repr__(self):
        return f"User('{self.email}', '{self.username}')"

# Test route to check if the server is working
@app.route('/api', methods=['GET'])
def test():
    return jsonify({"message": "Hello, this is your backend!"})

# Route to view user profile (returns first user)
@app.route('/user/profile', methods=["GET"])
def user_profile():
    user = User.query.first()  # Query the first user
    if not user:
        return jsonify({"message": "No User Found"}), 404
    return jsonify({"username": user.username, "email": user.email})

# Route to add a new user
@app.route('/user/add', methods=["POST"])
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

# Route to fetch all users
@app.route('/user/all', methods=["GET"])
def all_users():
    try:
        users = User.query.all()  # Query all users
        user_list = [{"username": user.username, "email": user.email} for user in users]
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"error":str(e)}),500

# Route to login (username and password)
@app.route('/user/login', methods=["POST"])
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

# Main entry point to run the Flask app
if __name__ == "__main__":
    os.environ["FLASK_ENV"] = "development"
    app.run(debug=True)
