# create_db.py
from app import app, db

# This creates the database and tables if they don’t exist
with app.app_context():
    db.create_all()

print("Database and tables created!")
