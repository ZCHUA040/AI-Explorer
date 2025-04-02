from sqlalchemy import or_
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt
from entity.models import db, User
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import base64

def get_user_profile(email):
    user = User.query.filter(User.email == email).first()

    if not user:
        return{"error" : "User not found"}, 404
    
    profile_image_b64 = (
        base64.b64encode(user.profile_image).decode('utf-8') if user.profile_image else None
    )

    return {
        "username" : user.username,
        "email" : user.email,
        "profile_image" : profile_image_b64
    }, 200

