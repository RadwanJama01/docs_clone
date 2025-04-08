from .users import user_bp
from .auth import auth_bp

all_routes= [auth_bp,user_bp]