from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_booking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key_here'

    db.init_app(app)
    migrate.init_app(app, db)

    # Register models
    from app import models

    # Register routes blueprint
    from app.routes import routes
    app.register_blueprint(routes)

    return app
