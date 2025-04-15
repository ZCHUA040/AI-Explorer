import sqlite3, json
import google.generativeai as genai
import os
import random
from dotenv import load_dotenv


def internal_get_my_itineraries(userid : int) -> list:
    """
    Function that retrieves all of 'my' itineraries 

    Args:
        int (userid): Userid of the itineraries that is being requested
        
    Returns:
        list: Each element is a JSON containing fields Itineraryid, Userid, Title, Date, Details, Created
    """
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve Itineraries
    raw_itineraries = conn.execute("SELECT * FROM Itineraries WHERE Userid = ?", (userid,)).fetchall()
    
    #Parse and format each itinerary into json
    output = []
    for raw_itinerary in raw_itineraries:
        itinerary = json.dumps({
            "Itineraryid" : raw_itinerary[0],
            "Userid" : raw_itinerary[1],
            "Title" : raw_itinerary[2],
            "Date" : raw_itinerary[3],
            "Details" : raw_itinerary[4],
            "Created" : raw_itinerary[5]
        })
        output.append(itinerary)
    
    #Close connection
    conn.close()
    
    return output



def internal_get_shared_itineraries(userid : int) -> list:
    """
    Function that retrieves all of itineraries shared with me

    Args:
        int (userid): Userid of the itineraries that is being requested
        
    Returns:
        list: Each element is a JSON containing fields Itineraryid, Userid, Title, Date, Details, Created
    """
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve Itineraries
    raw_itineraries = conn.execute("""
            SELECT i.*
            FROM Itineraries i
            JOIN SharedWith s ON i.Itineraryid = s.Itineraryid
            WHERE s.Sharedid = ?;
        """,(userid,)).fetchall()
    
    #Parse and format each itinerary into json
    output = []
    for raw_itinerary in raw_itineraries:
        itinerary = json.dumps({
            "Itineraryid" : raw_itinerary[0],
            "Userid" : raw_itinerary[1],
            "Title" : raw_itinerary[2],
            "Date" : raw_itinerary[3],
            "Details" : raw_itinerary[4],
            "Created" : raw_itinerary[5]
        })
        output.append(itinerary)
    
    #Close connection
    conn.close()
    
    return output



def internal_get_itinerary_by_itineraryid(itineraryid : int) -> str:
    """
    Function to retrieve a specific itinerary by itineraryid

    Args:
        int (itineraryid): Itineraryid of the itinerary that is being requested
        
    Returns:
        list: A JSON containing fields Itineraryid, Userid, Title, Date, Details, Created
    """
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve Itineraries
    raw_itinerary = conn.execute("SELECT * FROM Itineraries WHERE Itineraryid = ?", (itineraryid,)).fetchone()
    
    #Parse and format into json
    itinerary = json.dumps({
        "Itineraryid" : raw_itinerary[0],
        "Userid" : raw_itinerary[1],
        "Title" : raw_itinerary[2],
        "Date" : raw_itinerary[3],
        "Details" : raw_itinerary[4],
        "Created" : raw_itinerary[5]
    })

    
    #Close connection
    conn.close()
    
    return itinerary



def internal_update_itinerary(itineraryid : int, title : str, date : str, details : str) -> bool:
    """
    Function that updates a specific itinerary date/details based on the itineraryid

    Args:
        itineraryid (int): Itinerary identifier
        title (str): Title of itinerary
        date (str): Date of itinerary execution
        details (str): Specific schedule for itinerary

    Returns:
        bool: Status of Update
    """
    
    #Get connection
    conn = sqlite3.connect("test.db")
    
    #Perform update
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Itineraries
            SET Date = ?, Details = ?, Title = ?
            WHERE Itineraryid = ?;
        """, (date, details, title, itineraryid))
        
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return False
        
        conn.close()
        return True
    
    except Exception as e:
        conn.close()
        return False
    
    
    
def internal_delete_itinerary(userid : int, itineraryid : int) -> bool:
    """
    Function that deletes itinerary

    Args:
        userid (int): User identifier
        itineraryid (int): Itinerary identifier

    Returns:
        bool: Status of Delete
    """
    
    #Get connection
    conn = sqlite3.connect("test.db")
    
    #Perform delete
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Itineraries WHERE Itineraryid = ? AND Userid = ?", (itineraryid, userid))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return False
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False
    
    
    
def internal_generate_itinerary(userid : int, title : str, date : str, activity_type : str = None, price_category : str = None, start_time : str = "0800", end_time : str = "2100") -> str:
    """
        Function that generates an itineraries based on chosen filtered activities

    Args:
        int (userid): Userid of the itineraries that is being requested
        str (title): Title of itinerary
        str (date): Date of itinerary YYYY-MM-DD
        str (activity_type): Filter for activity, by default None
        str (price_category): Filter for activity, by default None
        str (start_time): Start time of itinerary, by default 0800
        str (end_time): End time of itinerary, by default 2100

    Returns:
        str : itinerary generated
    """
    
    # Configure Gemini API
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    

    # Define the activities list
    conn = sqlite3.connect("test.db")
    
    if activity_type and price_category:
        activities = conn.execute("SELECT Activityid, NAME FROM Activities WHERE Price_Category = ? AND Type = ?", (price_category,activity_type)).fetchall()
    elif activity_type:
        activities = conn.execute("SELECT Activityid, NAME FROM Activities WHERE Type = ?", (activity_type,)).fetchall()
    elif price_category:
        activities = conn.execute("SELECT Activityid, NAME FROM Activities WHERE Price_Category = ?", (price_category,)).fetchall()
    else:
        activities = conn.execute("SELECT Activityid, NAME FROM Activities").fetchall()
    random.shuffle(activities)
    if len(activities) == 0:
        return False

    # Prompt for the Gemini model
    prompt = f"""
        Create a detailed itinerary for a single day from {start_time} to {end_time} based on the following activities:
        - Have different type of activity of each slot
        - Each activity takes 2 hours.
        - Travel time between activities is 1 hour. (E.g. {{"time": "08:00-12:00","travel": "Travel from place A to place B"}})
        - Lunch should be scheduled for 2 hours. (Only if start time is before noon)
        - Lunch must occur at 1100 or 1200 or 1300. (E.g. {{"time": "08:00-12:00","lunch": "Lunch"}})
        - You need to travel to and from lunch. (E.g. {{"time": "08:00-12:00","travel": "Travel from place A to Lunch"}})
        - If there is less than 2 hours left, end itinerary.
        - Put the activity id beside the timeslot
        - Ensure a logical sequence.

        List of activities with their id:
        {activities}

        Output the itinerary in a structured json format with timeslots, do not include anything else.
        Sample output {{"time": "08:00-12:00", "id":1, "activity":"Swimming"}}
        """

    # Generate response
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt).text.strip("`").strip("json")

    
    #Create new itinerary
    cursor = conn.cursor()
    cursor.execute(
                   "INSERT INTO Itineraries (Userid, Title, Date, Details) VALUES (?, ?, ?, ?)",
                   (userid, title, date, response)
                   )
    conn.commit()
    
    #send itinerary back
    return {"Itineraryid" : cursor.lastrowid}



def internal_share_itinerary(userid : int, itineraryid : int, sharedname : int) -> bool:
    """
    Function to share an itinerary with other people

    Args:
        int (userid): Userid of sharer
        int (itineraryid): Itineraryid of current itinerary to share
        str (Sharename): Name of user to sharewith 

    Returns:
        str: Status of share
    """
    conn = sqlite3.connect("test.db")
    

    #Perform insertion
    try:
        #Get the userid of the name
        sharedid = conn.execute("SELECT Userid FROM User WHERE Name = ?",(sharedname,)).fetchone()[0]

        conn.execute(
            "INSERT INTO SharedWith (Userid, Itineraryid, Sharedid) VALUES (?, ?, ?)", 
            (userid, itineraryid, sharedid)
            )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False