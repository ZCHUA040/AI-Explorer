from flask import Blueprint, request
#from flask_jwt_extended import jwt_required, get_jwt_identity
from control.user_controller import UserController

user_api = Blueprint('user_api', __name__)
user_controller = UserController()

@user_api.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return{"error" : "Missing required fields"},400
    
    return user_controller.create_new_user(username,email,password)

@user_api.route("/login", methods=["POST"])  
def login():
    data = request.json
    identifier = data.get("identifier")
    password = data.get("password")

    if not identifier or not password:
        return{"error" : "Missing required fields"},400
    
    return user_controller.authenticate_user(identifier, password)
    



    
