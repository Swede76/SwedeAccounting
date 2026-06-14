import os
from flask_jwt_extended import JWTManager
from functools import wraps
from flask import request, jsonify

def setup_jwt(app):
    """Initialize JWT for the application"""
    jwt = JWTManager(app)
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        return {}
    
    return jwt

def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # TODO: Verify token and add user info to request context
        
        return f(*args, **kwargs)
    
    return decorated
