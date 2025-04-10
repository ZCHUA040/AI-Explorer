from flask_jwt_extended import create_access_token, decode_token
from flask import current_app
from flask_mail import Message
from datetime import timedelta
from extensions import bcrypt
import sqlite3, re

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

def forgot_password_request(email):
    try:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Email FROM User WHERE Email = ?", (email,))
        row = cursor.fetchone()
        conn.close()


        if not row:
            return {"error" : "Email not found"}, 404
        
        user_email = row[0]
    
        reset_token = create_access_token(
            identity=user_email,
            expires_delta=timedelta(hours=1),
            additional_claims={"type" : "password_reset"}
        )

        reset_link = f"http://localhost:5173/reset-password?token={reset_token}" ##change when the frontend link works

        msg = Message('Password Recovery/Reset',
                      sender = current_app.config['MAIL_USERNAME'],
                      recipients=[user_email]
                      )
        
        msg.body = f'''To reset your password, visit the follwoing link: {reset_link}
        if you did not make this request, please ignore this email
        '''
        current_app.extensions['mail'].send(msg)
        return {"Message" : "Password reset email sent"}, 200
    
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return {"error": "Failed to send email"}, 500
    
def reset_password(token,new_password):
        try:
            if not is_strong_password(new_password):
                return{"error" : "Password did not meet the requirement. It must be at least 8 characters long, include uppercase, lowercase, numbers, and special characters."}, 400
    
            decoded = decode_token(token)

            if decoded.get("type") != "password_reset":
                return {"error": "Invalid token"}, 400
            
            user_email = decoded["sub"].lower()

            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()

            cursor.execute("SELECT Userid FROM User WHERE Email = ?", (user_email,))
            row = cursor.fetchone()

            if not row:
                conn.close()
                return {"error": "User not found"}, 404
            
            user_id = row[0]

            new_hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')


            cursor.execute("UPDATE User SET Password = ? WHERE Userid = ?", (new_hashed_password, user_id))
            conn.commit()
            conn.close()

            return {"message": "Password reset successful"}, 200
        
        except Exception as e:
            return {"error": "Invalid or expired token", "details": str(e)}, 400

def change_password(user_id,current_password,new_password):
    try:
        if not current_password or not new_password:
            return {"error": "Missing password fields"}, 400
                    
        if not is_strong_password(new_password):
            return{"error" : "Password did not meet the requirement. It must be at least 8 characters long, include uppercase, lowercase, numbers, and special characters."}, 400

        # Connect to SQLite DB
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        # Get current hashed password from DB
        cursor.execute("SELECT Password FROM User WHERE Userid = ?", (user_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return {"error": "User not found"}, 404

        stored_hashed_password = row[0]

        # Check if current password is correct
        if not bcrypt.check_password_hash(stored_hashed_password, current_password):
            conn.close()
            return {"error": "Current password is incorrect"}, 401

        # Hash new password
        new_hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        # Update DB
        cursor.execute("UPDATE User SET Password = ? WHERE Userid = ?", (new_hashed_password, user_id))
        conn.commit()
        conn.close()

        return {"message": "Password changed successfully."}, 200

    except Exception as e:
        return {"error": "An error occurred", "details": str(e)}, 500