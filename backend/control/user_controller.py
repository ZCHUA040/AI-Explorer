from sqlalchemy import or_
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt
from entity.models import db, User
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

bcrypt = Bcrypt()

# Blacklist for revoked tokens (shared with app.py)
blacklist = set()

#Register User
def register_user(username, email, password):

    #Missing fields
    if not username or not email or not password:
        return{"error" : "Missing required fields"}, 400
    
    #Check for existig username or email in the database
    existing_user = User.query.filter((User.username == username) or (User.email == email)).first()

    if existing_user:
        if existing_user.username == username:
            return {"error": "Username already exists"}, 400 
        
        if existing_user.email == email:
            return {"error" : "Email already exists"}, 400 
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email = email, password_hash = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Account registered successfully"}, 201
    
    except Exception as e:
        db.session.rollback()
        return {"error": "User registration unsuccessful", "details": str(e)}, 500

def login_user(username,password):
    if not username:
        return{"error" : "Username is required"}, 400
    
    if not password:
        return{"error" : "Password is required"}, 400
    
    user = User.query.filter(User.username == username).first()

    if not user or not bcrypt.check_password_hash(user.password_hash , password):
        return{"error" : "Invalid email or password"}, 401
    
    access_token = create_access_token(identity=str(user.id))
    #print(f"Authorization: Bearer {access_token}") #debugging statement
    return {"message": "Login successful", "access_token": access_token}, 200
