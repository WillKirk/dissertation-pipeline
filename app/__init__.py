from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.files import files_bp
    from app.routes.templates import templates_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(templates_bp)
    
    with app.app_context():
        db.create_all()
    
    return app