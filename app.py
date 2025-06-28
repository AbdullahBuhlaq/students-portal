from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  # Add this import
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  # Initialize LoginManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)  # Initialize with app
    
    # Configure login settings
    login_manager.login_view = 'main.login'  # Specify login route
    login_manager.login_message_category = 'info'

    from routes import main_bp
    app.register_blueprint(main_bp)

    return app

import models