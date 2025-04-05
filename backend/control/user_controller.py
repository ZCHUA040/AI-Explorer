#from sqlalchemy import or_
import os
import sqlite3
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

bcrypt = Bcrypt()

# Blacklist for revoked tokens (shared with app.py)
blacklist = set()

#Register User 
#DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'test.db')

def register_user(username, email, password):
    if not username or not email or not password:
        return{"error" : "Missing required fields"}, 400

    try:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Name, Email FROM User WHERE Name = ? OR Email = ?", (username, email))
        existing = cursor.fetchone()

        if existing: 
            if existing[0] == username:
                return {"error": "Username already exists"}, 400
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
            return {"error": "Invalid email or password"}, 401
        
        user_id , name, email_db, hashed_password = row

        if not bcrypt.check_password_hash(hashed_password,password):
            return{"error" : "Invalid email or password"}, 401
        
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