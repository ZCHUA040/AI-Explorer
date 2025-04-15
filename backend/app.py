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
from extensions import bcrypt
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS


#DB
from control import recovery_account_controller
from control import user_controller
from control import activity_controller
from control import itinerary_controller

# Flask app setup https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
bcrypt.init_app(app)    #initialise bcrypt in flask app

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

#Configure JWT
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

#Configure SQLite Database
db_path = 'test.db' #change to remote desktop configuration (after testing )
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

# JWT Initialization
jwt = JWTManager(app)

# Blacklist to store revoked tokens
blacklist = set()
#----------------------------------------------Access Control related apis------------------------------------------

# Token blacklist check
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist

# Users Path
@app.route('/users')
def get_users():
    try: 
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor() 

        cursor.execute("SELECT Userid, Name, Password, Email FROM User")
        rows = cursor.fetchall()
        conn.close()

        users = []

        for row in rows:
            users.append({
                'userid': row[0],
                'name' : row[1],
                'password' : row[2],
                'email' : row[3]

            })

        return {'users' : users},200
    
    except Exception as e:
        return {'error' : str(e)},500

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
    email = data.get("email")
    password = data.get("password")
    return user_controller.login_user(email, password)
    # TODO: Implement login logic (For now, return a mock response)
    #return {"message": "Login successful", "email": email}, 200

#Current User
@app.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()

        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Name, Email FROM User WHERE Userid = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'name': row[0],
                'email': row[1]
            }, 200
        else:
            return {'error': 'User not found'}, 404

    except Exception as e:
        return {'error': str(e)}, 500
    
    
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

@app.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    return recovery_account_controller.change_password(user_id,current_password,new_password)

@app.route('/update-profile-picture', methods=['POST'])
@jwt_required()
def update_profile_icon():
    user_id = get_jwt_identity()
    data = request.json
    icon = data.get('icon')
    return user_controller.update_profile_icon(user_id, icon)

#----------------------------------------------Activity related apis------------------------------------------------

#Get all activities
@app.route("/get_all_activities", methods=["GET"])
#@jwt_required()
def get_all_activities():
    """
    Route: /get_all_activities
    Authentication: True
    Input: -
    Output: List of JSON objects, containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    return activity_controller.internal_get_all_activities(), 200
    

#Get activity by id (Activityid)
@app.route("/get_activity_by_id", methods=["POST"])
#@jwt_required()
def get_activity_by_id():
    """
    Route: /get_activity_by_id
    Authentication: True
    Input: id
    Output: One JSON object, containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    #Load and prep the activityid input
    data = request.json
    activityid = data.get("id")
    
    return activity_controller.internal_get_activity_by_id(activityid), 200


#Get activities by type ('Cultural & Heritage', 'Fitness & Wellness', 'Food & Beverage', 'Outdoor & Nature', 'Social & Community Events', 'Workshops & Classes')
@app.route("/get_activities_by_type", methods=["POST"])
#@jwt_required()
def get_activities_by_type():
    """
    Route: /get_activities_by_type
    Authentication: True
    Input: One of these types -> [
            'Cultural & Heritage', 
            'Fitness & Wellness', 
            'Food & Beverage', 
            'Outdoor & Nature', 
            'Social & Community Events', 
            'Workshops & Classes'
            ]
    Output: List of JSON objects, containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    
    #Process type input
    data = request.json
    type = data.get("Type")
    
    #Validate type
    all_types = [
            'Cultural & Heritage', 
            'Fitness & Wellness', 
            'Food & Beverage', 
            'Outdoor & Nature', 
            'Social & Community Events', 
            'Workshops & Classes'
            ]
    if type not in all_types:
        return {"Error": "Invalid type given"}, 400
    
    
    return activity_controller.internal_get_activities_by_type(type), 200


#Get activities by price category
@app.route("/get_activities_by_price_category", methods=["POST"])
#@jwt_required()
def get_activities_by_price_category():
    """
    Route: /get_activities_by_price_category
    Authentication: True
    Input: One of these categories -> [
            'Free', 
            '$', 
            '$$', 
            '$$$', 
            ]
    Output: List of JSON objects, containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    #Process price category input
    data = request.json
    price_category = data.get("Price Category")
    
    #Validate category
    all_categories = [
            "Free", 
            "$", 
            "$$", 
            "$$$", 
            ]
    if price_category not in all_categories:
        return {"Error": "Invalid price category given"}, 400
    
    
    return activity_controller.internal_get_activities_by_price_category(price_category), 200


#Get activities by price category
@app.route("/get_activities_by_type_and_price_category", methods=["POST"])
#@jwt_required()
def get_activities_by_type_and_price_category():
    """
    Route: /get_activities_by_type_and_price_category
    Authentication: True
    Input: 
        One of these types -> [
            'Cultural & Heritage', 
            'Fitness & Wellness', 
            'Food & Beverage', 
            'Outdoor & Nature', 
            'Social & Community Events', 
            'Workshops & Classes'
            ]
        
        One of these categories -> [
            'Free', 
            '$', 
            '$$', 
            '$$$', 
            ]
    Output: List of JSON objects, containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    #Process price category input
    data = request.json
    price_category = data.get("Price Category")
    type = data.get("Type")
    
    #Validate type
    all_types = [
            'Cultural & Heritage', 
            'Fitness & Wellness', 
            'Food & Beverage', 
            'Outdoor & Nature', 
            'Social & Community Events', 
            'Workshops & Classes'
            ]
    if type not in all_types:
        return {"Error": "Invalid type given"}, 400
    
    #Validate category
    all_categories = [
            "Free", 
            "$", 
            "$$", 
            "$$$", 
            ]
    if price_category not in all_categories:
        return {"Error": "Invalid price category given"}, 400
    
    
    return activity_controller.internal_get_activities_by_type_and_price_category(type, price_category), 200



#----------------------------------------------Itinerary related apis------------------------------------------------
'''
@app.route("/get_my_itineraries", methods=["POST"])
@jwt_required()
def get_my_itineraries():
    """
    Route: /get_my_itineraries
    Authentication: True
    Input: Userid of current user
    Output: Each element is a JSON containing fields Itineraryid, Userid, Title, Date, Details, Created
    """
    #Retrieve userid
    data = request.json
    userid = data["Userid"]
    
    return itinerary_controller.internal_get_my_itineraries(userid), 200
'''

@app.route("/get_my_itineraries", methods=["POST"])
@jwt_required()
def get_my_itineraries():
    """
    Route: /get_my_itineraries
    Authentication: True
    Input: Userid of current user
    Output: Each element is a JSON containing fields Itineraryid, Userid, Title, Date, Details, Created
    """
    #Retrieve userid
    userid = get_jwt_identity() 
    print(f"JWT decoded successfully: {userid}")
    return itinerary_controller.internal_get_my_itineraries(userid), 200
'''
@app.route("/get_shared_itineraries", methods=["POST"])
@jwt_required()
def get_shared_itineraries():
    """
    Route: /get_shared_itineraries
    Authentication: True
    Input: Userid of current user
    Output: Each element is a JSON containing fields Itineraryid, Userid, Title, Date, Details, Created
    """
    #Retrieve userid
    data = request.json
    userid = data["Userid"]
    
    return itinerary_controller.internal_get_shared_itineraries(userid), 200
'''
@app.route("/get_shared_itineraries", methods=["POST"])
@jwt_required()
def get_shared_itineraries():
    """
    Route: /get_shared_itineraries
    Authentication: True
    Input: Userid of current user
    Output: Each element is a JSON containing fields Itineraryid, Userid, Title, Date, Details, Created
    """
    #Retrieve userid
    #data = request.json
    userid = get_jwt_identity() 
    
    return itinerary_controller.internal_get_shared_itineraries(userid), 200



@app.route("/get_itinerary_by_itineraryid", methods=["POST"])
@jwt_required()
def get_itinerary_by_itineraryid():
    """
    Route: /get_itinerary_by_itineraryid
    Authentication: True
    Input: Itineraryid of itinerary requested
    Output: A JSON containing fields Itineraryid, Userid, Title, Date, Details, Created
    """
    #Retrieve itineraryid
    data = request.json
    itineraryid = data["Itineraryid"]
    
    return itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid), 200


@app.route("/update_itinerary", methods=["POST"]) 
@jwt_required()
def update_itinerary():
    """
    Route: /update_itinerary
    Authentication: True
    Input: Itineraryid of itinerary requested, Title, Date, Details
    Output: Status of action
    """
    #Retrieve itineraryid
    data = request.json
    itineraryid = data["Itineraryid"]
    title = data["Title"]
    date = data["Date"]
    details = data["Details"]
    
    status = itinerary_controller.internal_update_itinerary(itineraryid, title, date, details)
    
    if status:
        return {"Status" : "Success"}, 200
    
    return {"Status" : "Error"}, 500


@app.route("/delete_itinerary", methods=["POST"])
@jwt_required()
def delete_itinerary():
    """
    Route: /delete_itinerary
    Authentication: True
    Input: Itineraryid to delete, Userid
    Output: Status of action
    """
    data = request.json
    itineraryid = data["Itineraryid"]
    userid = data["Userid"]
    
    status = itinerary_controller.internal_delete_itinerary(userid, itineraryid)
    
    if status:
        return {"Status" : "Success"}, 200
    
    return {"Status" : "Error"}, 500

'''    
@app.route("/generate_itinerary", methods=["POST"])
@jwt_required()
def generate_itinerary():
    """
    Route: /generate_itinerary
    Authentication: True
    Input:   
        int (userid): Userid of the itineraries that is being requested
        str (title): Title of itinerary
        str (date): Date of itinerary YYYY-MM-DD
        str (activity_type): Filter for activity, by default None
        str (price_category): Filter for activity, by default None
        str (start_time): Start time of itinerary, by default 0800
        str (end_time): End time of itinerary, by default 2100
    Output: Generated itineraryid
    """
    #Get inputs
    data = request.json
    userid = data["userid"]
    title = data["title"]
    date = data["date"]
    activity_type = data["activity_type"]
    price_category = data["price_category"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    
    return itinerary_controller.internal_generate_itinerary(userid, title, date, activity_type, price_category, start_time, end_time)
'''    
@app.route("/generate_itinerary", methods=["POST"])
@jwt_required()
def generate_itinerary():
    """
    Route: /generate_itinerary
    Authentication: True
    Input:   
        int (userid): Userid of the itineraries that is being requested
        str (title): Title of itinerary
        str (date): Date of itinerary YYYY-MM-DD
        str (activity_type): Filter for activity, by default None
        str (price_category): Filter for activity, by default None
        str (start_time): Start time of itinerary, by default 0800
        str (end_time): End time of itinerary, by default 2100
    Output: Generated itineraryid
    """
    #Get inputs
    data = request.json
    userid = get_jwt_identity()
    title = data["title"]
    date = data["date"]
    activity_type = data["activity_type"]
    price_category = data["price_category"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    
    if activity_type == "":
        activity_type = None
    if price_category == "":
        price_category = None
    itinerary = itinerary_controller.internal_generate_itinerary(userid, title, date, activity_type, price_category, start_time, end_time)
    if itinerary:
        return itinerary
    return {"Error": "No such activities"}, 500
    
@app.route("/share_itinerary", methods=["POST"])
@jwt_required()
def share_itinerary():
    """
    Route: /generate_itinerary
    Authentication: True
    Input:   
        int (userid): Userid of sharer
        int (itineraryid): Itineraryid of current itinerary to share
        str (Sharename): Name of user to sharewith 
    Output: Success or Failure
    """
    #Get inputs
    data = request.json
    userid = get_jwt_identity() 
    itineraryid = data["Itineraryid"]
    sharename = data["shareName"]
    
    status = itinerary_controller.internal_share_itinerary(userid, itineraryid, sharename)

    if status:
        return {"Status" : "Success"}, 200
    
    return {"Status" : "Error"}, 500


'''    
@app.route("/share_itinerary", methods=["POST"])
@jwt_required()
def share_itinerary():
    """
    Route: /generate_itinerary
    Authentication: True
    Input:   
        int (userid): Userid of sharer
        int (itineraryid): Itineraryid of current itinerary to share
        str (Sharename): Name of user to sharewith 
    Output: Success or Failure
    """
    #Get inputs
    data = request.json
    userid = data["Userid"]
    itineraryid = data["Itineraryid"]
    sharename = data["shareName"]
    
    status = itinerary_controller.internal_share_itinerary(userid, itineraryid, sharename)

    if status:
        return {"Status" : "Success"}, 200
    
    return {"Status" : "Error"}, 500
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    #app.debug = False
    
    #for normal local testing use this run
    app.run(host='127.0.0.1', port=port, debug=True)
    
    #For Deployment
    #app.run(host='0.0.0.0', port=port, debug=True)