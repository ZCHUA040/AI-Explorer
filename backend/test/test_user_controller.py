import sys
import os
import bcrypt
from flask import Flask 
from flask_jwt_extended import JWTManager 

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import UserController
from backend.control.user_controller import UserController  

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
jwt = JWTManager(app)

user_controller = UserController()

print("\nTest Case 1: Registering a New User")
response, status = user_controller.create_new_user("john_doe", "john@example.com", "securepass")
print(response)  

print("\nTest Case 2: Registering with Existing Username")
response, status = user_controller.create_new_user("john_doe", "john2@example.com", "securepass")
print(response) 

print("\nTest Case 3: Registering with Existing Email")
response, status = user_controller.create_new_user("new_user", "john@example.com", "securepass")
print(response)  

print("\nTest Case 4: Registering with Missing Fields")
response, status = user_controller.create_new_user("", "missing@example.com", "")
print(response)  

with app.app_context():  
    print("\nTest Case 5: Login with Correct Username and Password")
    response, status = user_controller.authenticate_user("john_doe", "securepass")
    print(response)  

    print("\nTest Case 6: Login with Correct Email and Password")
    response, status = user_controller.authenticate_user("john@example.com", "securepass")
    print(response)  

    print("\nTest Case 7: Login with Incorrect Password")
    response, status = user_controller.authenticate_user("john_doe", "wrongpassword")
    print(response) 

    print("\nTest Case 8: Login with Non-Existent User")
    response, status = user_controller.authenticate_user("unknown_user", "securepass")
    print(response) 
