from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from application.admin import MyAdmin

# Globally accessible libraries
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
my_admin = MyAdmin()

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Setup Flask-Admin
    my_admin.init_admin(app, db)

    # Import blueprints
    from application.home import home_bp
    from application.auth import auth_bp
    from application.blog import blog_bp

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    
    return app

