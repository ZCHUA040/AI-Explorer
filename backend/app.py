#Default libraries
import json
import os
from datetime import datetime, timedelta
from routes.userAPI import user_api  

#PSQL
import psycopg2

#Flask
from flask import Flask, request, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt


# Flask app setup https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

#Configure JWT
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

# JWT Initialization
jwt = JWTManager(app)

app.register_blueprint(user_api) 

# Blacklist to store revoked tokens
blacklist = set()

# Token blacklist check
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist


#Register Path
'''
@app.route('/register', methods=['POST'])
##jwt_required
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    # TODO: Implement user registration logic (For now, return a success response)
    return {"message": "User registered successfully", "username": username}, 201
'''

#Login Path
'''
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # TODO: Implement login logic (For now, return a mock response)
    return {"message": "Login successful", "email": email}, 200'
'''
#Logout Path
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    data = request.json
    username = data["Username"]
    
    jti = get_jwt()['jti']  # JWT ID
    blacklist.add(jti)  # Add the token's jti to the blacklist
    
    return {'Message': 'Successfully logged out'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    #app.debug = False
    
    #for normal local testing use this run
    app.run(host='127.0.0.1', port=port, debug=True)
    
    #For Deployment
    #app.run(host='0.0.0.0', port=port, debug=True)