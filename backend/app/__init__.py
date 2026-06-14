from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import auth_bp, invoice_bp, bookkeeping_bp, reporting_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(bookkeeping_bp)
    app.register_blueprint(reporting_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
