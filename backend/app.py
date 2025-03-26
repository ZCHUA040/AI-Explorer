#Default libraries
import json
import os
from datetime import datetime, timedelta

#PSQL
import psycopg2

#SQLite
import sqlite3

#Flask
from flask import Flask, request, send_file, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


#DB
from control import recovery_account_controller
from control import user_controller
from entity.models import db, User, Session

# Flask app setup https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

#Configure JWT
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

#Configure SQLite Database
db_path = r'C:\Users\chuaz\OneDrive\Desktop\SC2006\database.db' #change to remote desktop configuration (after testing )
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Configure mailbox
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sc2006.scsb.t5@gmail.com'
app.config['MAIL_PASSWORD'] = 'vado ihip dmkz xjvs'
app.config['MAIL_DEFAULT_SENDER'] = 'sc2006.scsb.t5@gmail.com'
mail = Mail(app)

# Initialize SQLAlchemy
db.init_app(app)

# JWT Initialization
jwt = JWTManager(app)

# Blacklist to store revoked tokens
blacklist = set()

# Token blacklist check
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist

# Users Path
@app.route('/users')
def get_users():
    users = User.query.all()
    return {'users': [{'id': user.id, 'username': user.username, 'email': user.email, 'password' : user.password_hash} for user in users]}

#Register Path
@app.route('/register', methods=['POST'])
##jwt_required
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    return user_controller.register_user(username, email, password)
    # TODO: Implement user registration logic (For now, return a success response)

#Login Path
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    return user_controller.login_user(username, password)
    # TODO: Implement login logic (For now, return a mock response)
    #return {"message": "Login successful", "email": email}, 200

#Logout Path
@app.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():    
    jti = get_jwt()['jti']  # JWT ID
    blacklist.add(jti)  # Add the token's jti to the blacklist
    return {'Message': 'Successfully logged out'}, 200

#Validate session for user path
@app.route('/validateuserlogin', methods=['GET'])
@jwt_required()
def validate_session():
    try:
        current_user_id = get_jwt_identity()
        return {"message": f"Hello User {current_user_id}, this is a protected route!"}, 200
    
    except Exception as e:
        return {"error": str(e)}, 401
    

#Recovery Account - Password Reset Path
@app.route('/forgot-password', methods=['POST'])   
def forgot_password():
    data = request.json
    email = data.get("email")
    return recovery_account_controller.forgot_password_request(email)

@app.route('/reset-password', methods=['POST'])   
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = request.json.get("new_password")
    return recovery_account_controller.reset_password(token,new_password)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    port = int(os.environ.get('PORT', 5000))
    #app.debug = False
    
    #for normal local testing use this run
    app.run(host='127.0.0.1', port=port, debug=True)
    
    #For Deployment
    #app.run(host='0.0.0.0', port=port, debug=True)