import unittest
from flask import Flask
from flask_testing import TestCase
import os
import sys

# Add the project root directory to sys.path for imports to work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from backend.routes.userAPI import user_api  # Import the user API blueprint

class TestUserAPIIntegration(TestCase):
    def create_app(self):
        # Set up a Flask app for testing
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
        app.register_blueprint(user_api, url_prefix="/api/user")
        return app
        #self.client = self.app.test_client()

    def test_register_user(self):
        # Test successful registration
        response = self.client.post("/api/user/register", json={
            "username": "john_doe",
            "email": "john@example.com",
            "password": "securepass"
        })
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "User created successfully")
    

if __name__ == "__main__":
    unittest.main()
