from flask_jwt_extended import create_access_token, decode_token
from flask import current_app
from flask_mail import Message
from datetime import timedelta
from entity.models import db, User
import bcrypt

def forgot_password_request(email):
    user = User.query.filter(User.email == email).first()

    if not user:
        return {"error" : "Email not found"}, 404
    
    reset_token = create_access_token(
        identity = user.email,
        expires_delta=timedelta(hours=1),
        additional_claims={"type" : "password_reset"}
    )

    reset_link = f"http://your-frontend.com/reset-password?token={reset_token}" ##change when the frontend link works
    
    try:
        msg = Message('Password Recovery/Reset',
                      sender = current_app.config['MAIL_USERNAME'],
                      recipients=[user.email])
        
        msg.body = f'''To reset your password, visit the follwoing link: {reset_link}
        if you did not make this request, please ignore this email
        '''
        current_app.extensions['mail'].send(msg)
        return {"Message" : "Password reset email sent"}, 200
    
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return {"error": "Failed to send email"}, 500
        
def reset_password(token, new_password):
    try:
        decoded = decode_token(token)
        if decoded.get("type") != "password_reset":
            return {"error": "Invalid token"}, 400
        
        user = User.query.filter(User.email == decoded["sub"]).first()
        if not user:
            return{"error" : "User not found"}, 404
        
        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        return {"message": "Password reset successful"}, 200

    except Exception as e:
        return {"error": "Invalid or expired token"}, 400


