from flask import Blueprint, request, current_app
from control.recover_account_controller import RecoverAccountController

recover_account_api = Blueprint('recover_account_api', __name__)
recover_account_controller = RecoverAccountController(user_controller.user, mail)

@recover_account_api.route("/recovery-account",method = ["POST"])
def send_recover_email():
    data = request.json
    email = data.get("email")

    if not email:
        return{"error" : "Email is required"}, 400 
    
    return recover_account_controller.send_recover_email(email)

@recover_account_api.route("/reset-password", method = ["POST"])
def reset_password():
    data = request.json
    token = data.get("token")
    email = data.get("email")
    new_password = data.get("new_password")

    if not email or not token or not new_password:
        return {"error" : "Missing required fields"}, 400
    
    return recover_account_controller.reset_password(email, token, new_password)



