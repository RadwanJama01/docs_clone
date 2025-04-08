from app import db
from werkzeug.security import generate_password_hash,check_password_hash



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
