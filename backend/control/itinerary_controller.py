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
        list: Each element is a JSON containing fields Itineraryid, Userid, Date, Details, Created
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
            "Date" : raw_itinerary[2],
            "Details" : raw_itinerary[3],
            "Created" : raw_itinerary[4]
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
        list: Each element is a JSON containing fields Itineraryid, Userid, Date, Details, Created
    """
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve Itineraries
    raw_itineraries = conn.execute(""""
            SELECT i.*
            FROM Itineraries i
            JOIN SharedWith s ON i.Itineraryid = s.Itineraryid
            WHERE s.SharedUserid = ?;
        """,(userid,)).fetchall()
    
    #Parse and format each itinerary into json
    output = []
    for raw_itinerary in raw_itineraries:
        itinerary = json.dumps({
            "Itineraryid" : raw_itinerary[0],
            "Userid" : raw_itinerary[1],
            "Date" : raw_itinerary[2],
            "Details" : raw_itinerary[3],
            "Created" : raw_itinerary[4]
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
        list: A JSON containing fields Itineraryid, Userid, Date, Details, Created
    """
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve Itineraries
    raw_itinerary = conn.execute("SELECT * FROM Itineraries WHERE Itineraryid = ?", (itineraryid,)).fetchone()
    
    #Parse and format into json
    itinerary = json.dumps({
        "Itineraryid" : raw_itinerary[0],
        "Userid" : raw_itinerary[1],
        "Date" : raw_itinerary[2],
        "Details" : raw_itinerary[3],
        "Created" : raw_itinerary[4]
    })

    
    #Close connection
    conn.close()
    
    return itinerary



def internal_update_itinerary(itineraryid : int, date : str, details : str) -> bool:
    """
    Function that updates a specific itinerary date/details based on the itineraryid

    Args:
        itineraryid (int): Itinerary identifier
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
            SET Date = ?, Details = ?
            WHERE Itineraryid = ?;
        """, (date, details, itineraryid))
        
        conn.commit()
        
        conn.close()
        return True
    
    except:
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
        conn.execute("DELETE FROM Itineraries WHERE Itineraryid = ? AND Userid = ?", (itineraryid, userid))
        conn.close()
        return True
    except:
        conn.close()
        return False
    
    
    
def internal_generate_itinerary(userid : int, date : str, activity_type : str = None, price_category : str = None, start_time : str = "0800", end_time : str = "2100") -> str:
    """
        Function that generates an itineraries based on chosen filtered activities

    Args:
        int (userid): Userid of the itineraries that is being requested
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


    # Prompt for the Gemini model
    prompt = f"""
        Create a detailed itinerary for a single day from {start_time} to {end_time} based on the following activities:
        - Have different type of activity of each slot
        - Each activity takes 2 hours.
        - Travel time between activities is 1 hour.
        - Lunch should be scheduled for 2 hours. (Only if start time is before noon)
        - Lunch must occur at 1100 or 1200 or 1300.
        - You need to travel to and from lunch.
        - If there is less than 2 hours left, end itinerary.
        - Put the activity id beside the timeslot
        - Ensure a logical sequence.

        List of activities with their id:
        {activities}

        Output the itinerary in a structured json format with timeslots, do not include anything else.
        Sample output {{"time": "0800-1200", "id":1, "activity":"Swimming"}}
        """

    # Generate response
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    #Format into JSON
    json_itinerary = json.loads(response.text.strip("`").strip("json"))
    
    #Create new itinerary
    cursor = conn.cursor()
    cursor.execute(
                   "INSERT INTO Itineraries (Userid, Date, Details) VALUES (?, ?, ?)",
                   (userid, date, json_itinerary)
                   )
    conn.commit()
    
    #send itinerary back
    return internal_get_itinerary_by_itineraryid(cursor.lastrowid)