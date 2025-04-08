from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/rjama/flask-backend/instance/site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app,db)
    
    from app.routes.auth import auth_bp
    from app.routes.users import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    
    return app
    
