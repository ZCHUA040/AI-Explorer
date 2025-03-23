import uuid
from datetime import datetime, timedelta
from flask_mail import Message
from flask import url_for
import bcrypt

class RecoverAccountController:
    def __init__(self, users, mail):
        self.users = users
        self.recovery_tokens = {}
        self.mail = mail

    def send_recover_email(self, email , host_url):
        user_id = next((uid for uid, details in self.users.items() if details["emails"] == email), None)

        if not user_id:
            return {"message" : "if the email exist, a recovery email has been sent"}, 200
        
        recovery_token = str(uuid.uuid4)
        expiry_time = datetime.now() + timedelta(minutes = 40)
        self.recovery_tokens[email] = {"token" : recovery_token , "expiry" : expiry_time}
        reset_link = f"{host_url}/reset-password/{recovery_token}"

        # Send the recovery email using Flask-Mail
        try:
            msg = Message(
                subject="Password Recovery",
                recipients=[email],
                body=f"Hello,\n\nClick the link below to reset your password:\n\n{reset_link}\n\n"
                     f"This link will expire in 40 minutes.\n\nIf you did not request this, please ignore this message."
            )
            self.mail.send(msg)
            return {"message": "If the email exists, a recovery email has been sent"}, 200
        except Exception as e:
            return {"error": "Failed to send recovery email", "details": str(e)}, 500
        
    def reset_password(self,email , token, new_password):
        email = next((email for email, details in self.recovery_tokens.items() if details["token"] == token))
        if not email or self.recovery_tokens[email]["expiry"] < datetime.now():
            return {"error" : "Invalid or expired token"}, 400
        
        user_id = next((uid for uid, details in self.users.items() if details["emails"] == email), None)
        if not user_id:
            return {"error" : "Email not found"}, 400
        
        hashed_password = bcrypt.hashpw(new_password.encode(),bcrypt.gensalt()).decode()
        self.users[user_id]["password"] = hashed_password

        del self.recovery_tokens[email]

        return {"message" : "Password reset successful"}, 200          
