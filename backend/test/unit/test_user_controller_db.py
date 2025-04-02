import sys
import os
from flask import Flask
from flask_jwt_extended import JWTManager

# Add the project root directory to sys.path for imports to work correctly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from backend.control.user_controller_db import UserController  # Import UserController
from backend.entity.models import User


import unittest

class TestUserController(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite:///:memory"
        self.app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
        self.jwt = JWTManager(self.app)
        self.user_controller = UserController()

    def test_create_new_user(self): 
        response, status = self.user_controller.create_new_user("john_doe", "john@example.com", "securepass")
        self.assertEqual(status, 201)
        self.assertEqual(response['message'], 'User created successfully')
    
    def test_duplicate_username(self):
        self.user_controller.create_new_user("john_doe", "john2@example.com", "securepass")
        response, status = self.user_controller.create_new_user("john_doe", "john2@example.com", "securepass")
        self.assertEqual(status, 400)
        self.assertEqual(response['error'], 'Username already exists')
            
    def test_duplicate_email(self):
        self.user_controller.create_new_user("john_doe1", "john@example.com", "securepass")
        response, status = self.user_controller.create_new_user("john_doe2", "john@example.com", "securepass")
        self.assertEqual(status, 400)
        self.assertEqual(response['error'], 'Email already exists')

    def test_missing_fields(self):
        response, status = self.user_controller.create_new_user("", "john@example.com","securepass") # missing username field
        self.assertEqual(status, 400)
        self.assertEqual(response['error'], 'Missing required fields')

        response, status = self.user_controller.create_new_user("john_doe", "","securepass") # missing email field
        self.assertEqual(status, 400)
        self.assertEqual(response['error'], 'Missing required fields')

        response, status = self.user_controller.create_new_user("john_doe", "john@example.com","") # missing password field
        self.assertEqual(status, 400)
        self.assertEqual(response['error'], 'Missing required fields')

        response, status = self.user_controller.create_new_user("", "","") # missing all fields
        self.assertEqual(status, 400)
        self.assertEqual(response['error'], 'Missing required fields')

    def test_authentic_valid_credentials(self):
        with self.app.app_context():
            self.user_controller.create_new_user("john_doe", "john@example.com", "securepass")

        #login with username
            response, status = self.user_controller.authenticate_user("john_doe", "securepass")
            self.assertEqual(status, 200)
            self.assertIn('access_token' , response)

        #login with email
            response, status = self.user_controller.authenticate_user("john@example.com", "securepass")
            self.assertEqual(status, 200)
            self.assertIn('access_token' , response)

        #login with invalid email
            response, status = self.user_controller.authenticate_user("john1@example.com", "securepass")
            self.assertEqual(status, 404)
            self.assertEqual(response['error'], 'User not found')

        #login with invalid username
            response, status = self.user_controller.authenticate_user("john_doe1", "securepass")
            self.assertEqual(status, 404)
            self.assertEqual(response['error'], 'User not found')

        #login with invalid password
            response, status = self.user_controller.authenticate_user("john_doe", "securepass1")
            self.assertEqual(status, 401)
            self.assertEqual(response['error'], 'Invalid password')

    
    def test_password_hashing(self):
        response, status = self.user_controller.create_new_user("john_doe", "john@example.com", "securepass")
        self.assertEqual(status, 201)
    
        # Extract the stored user data
        user_id = next(iter(self.user_controller.users.keys()))  # Get the first user ID
        stored_password = self.user_controller.users[user_id]["password"]
            
        # Ensure the stored password is not the same as the plaintext password
        self.assertNotEqual(stored_password, "securepass")

if __name__ == "__main__":
    unittest.main() 
