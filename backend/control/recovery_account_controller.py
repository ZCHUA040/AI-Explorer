from flask_jwt_extended import create_access_token, decode_token
from flask import current_app
from flask_mail import Message
from datetime import timedelta
from entity.models import db, User
from app import bcrypt 

def forgot_password_request(email):
    user = User.query.filter(User.email == email).first()

    if not user:
        return {"error" : "Email not found"}, 404
    
    reset_token = create_access_token(
        identity=user.email,
        expires_delta=timedelta(hours=1),
        additional_claims={"type" : "password_reset"}
    )

    reset_link = f"http://localhost:5173/reset-password?token={reset_token}" ##change when the frontend link works
    
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
        #print("1")
        if decoded.get("type") != "password_reset":
            return {"error": "Invalid token"}, 400
        #print("2")        
        user = User.query.filter(User.email == decoded["sub"].lower()).first()
        #print("3")
        if not user:
            return{"error" : "User not found"}, 404
        #print("4")
        
        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        #print("5")
        db.session.commit()
        #print("6")                                 #debugging statement to find where exactly the code stop runnning
        return {"message": "Password reset successful"}, 200

    except Exception as e:
        #print("Exception in reset_password:", e)   #debugging statement to find the exact error
        return {"error": "Invalid or expired token"}, 400


