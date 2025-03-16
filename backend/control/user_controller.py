import bcrypt
from flask_jwt_extended import create_access_token

class UserController:
    def __init__(self):
        self.users = {}    #temporary database (dictionary), will integrate POSTGRESQL schema

    def create_new_user(self, username, useremail, userpassword):

        if username in self.users:
            return {"error" : "Username already exists"}, 400  #validate if username exist
        
        if any(user["email"] == useremail for user in self.users.values()):
            return {"error" : "Email already exists"}, 400     #validate if email exist

        if not username or not useremail or not userpassword:
            return {"error": "Missing required fields"}, 400   #validate missing fields
                
        hashed_secure_pw = bcrypt.hashpw(userpassword.encode(), bcrypt.gensalt()).decode()

        self.users[username] = {
        "email": useremail,
        "password": hashed_secure_pw
        }
        return {"message": "User created successfully"}, 201
    
    def authenticate_user(self, identity, password):
        if not identity or not password:
            return {"error": "Username/email and password are required"}, 400
        
        user = None
        username_match = None

        for uname, details in self.users.items():
            if uname == identity or details['email'] == identity:
                user = details
                username_match = uname
                break

        if not user:
            return {"error" : "User not found"}, 404
        
        try:
            if not bcrypt.checkpw(password.encode(), user["password"].encode()):
                return {"error": "Invalid password"}, 401
            
        except Exception as e:
            return {"error": "Authentication error", "details": str(e)}, 500
        
        access_token = create_access_token(identity=username_match)

        return {
            "message": "Login successful", 
            "access_token": access_token,
            "username": username_match  
        }, 200       
