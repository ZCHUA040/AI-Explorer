#from sqlalchemy import or_
import os
import re
import sqlite3
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from email_validator import validate_email


bcrypt = Bcrypt()

# Blacklist for revoked tokens (shared with app.py)
blacklist = set()

#Register User 
#DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'test.db')

def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


def register_user(username, email, password):
    if not username or not email or not password:
        return{"error" : "Missing required fields"}, 400
    
    try:
        valid = validate_email(email)
        email = valid.email
    except Exception as e:
        return {"error": "User registration unsuccessful, Email is invalid "}, 400
    
    if not is_strong_password(password):
        return{"error" : "Password did not meet the requirement. It must be at least 8 characters long, include uppercase, lowercase, numbers, and special characters"}, 400

    try:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Name, Email FROM User WHERE Name = ? OR Email = ?", (username, email))
        existing = cursor.fetchone()

        if existing: 
            if existing[0] == username:
                return {"error": "Name already exists"}, 400
            if existing[1] == email:
                return {"error" : "Email already exists"}, 400 
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        default_image = b''

        #Insert New User
        cursor.execute(
            "INSERT INTO User (Name, Password, Email, UserImage) VALUES (?, ?, ?, ?)",
            (username, hashed_password, email, default_image )
        )
        conn.commit()
        conn.close()

        return {"message": "Account registered successfully"}, 201
    
    except Exception as e:
        return {"error": "User registration unsuccessful", "details": str(e)}, 500

def login_user(email,password):
    if not email:
        return{"error" : "Email is required"}, 400
    
    if not password:
        return{"error" : "Password is required"}, 400
    
    try:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        # Fetch user by email
        cursor.execute("SELECT Userid, Name, Email, Password FROM User WHERE Email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {"error": "Email not found and/or incorrect password"}, 401
        
        user_id , name, email_db, hashed_password = row

        if not bcrypt.check_password_hash(hashed_password,password):
            return{"error" : "Email not found and/or incorrect password"}, 401
        
        access_token = create_access_token(identity=str(user_id))

        return {
            "message": "Login successful",
            "access_token": access_token,
            "user_id": user_id,
            "name": name,
            "email": email_db
        }, 200
    
    
    except Exception as e:
        return {"error": "Login failed", "details": str(e)}, 500