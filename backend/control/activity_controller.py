import sqlite3, json
import random

def internal_get_all_activities() -> list:
    """
    Function that retreives all activites in Activities Table

    Returns:
        list: Each element is a JSON containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    
    #Get Connection
    conn = sqlite3.connect("test.db")
    
    #Retrieves activities   
    activites = conn.execute("SELECT * FROM Activities;").fetchall()
    
    #Format the output in proper format
    output = []
    for activity in activites:
        element = json.dumps({
            "Activityid" : activity[0],
            "Name" : activity[1],
            "Type" : activity[2],
            "Location" : activity[3],
            "Price" : activity[4],
            "Price Category" : activity[5],
            "Image" : activity[6],
            "Description" : activity[7]
        })
        output.append(element)
        
    #Close connection
    conn.close()
    random.shuffle(output)
    return output



def internal_get_activity_by_id(id : int) -> str:
    """
    Function that returns a single activity based on the activity id.

    Args:
        int (id): Activityid of the activity that is being requested

    Returns:
        str: JSON containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve activity
    raw_activity = conn.execute("SELECT * FROM Activities WHERE Activityid = ?;", (id,)).fetchone()

    #Format activity into JSON format
    activity = json.dumps({
        "Activityid" : raw_activity[0],
        "Name" : raw_activity[1],
        "Type" : raw_activity[2],
        "Location" : raw_activity[3],
        "Price" : raw_activity[4],
        "Price Category" : raw_activity[5],
        "Image" : raw_activity[6],
        "Description" : raw_activity[7]
    })
    
    #Close connection
    conn.close()
    
    return activity



def internal_get_activities_by_type(type : str) -> list:
    """
    Function that retrieves all activities of requested type.

    Args:
        type (str): One of these types -> [
            'Cultural & Heritage', 
            'Fitness & Wellness', 
            'Food & Beverage', 
            'Outdoor & Nature', 
            'Social & Community Events', 
            'Workshops & Classes'
            ]

    Returns:
        list: Each element is a JSON containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve activity
    raw_activities = conn.execute("SELECT * FROM Activities WHERE Type = ?;", (type,)).fetchall()

    #Format activity into JSON format
    output = []
    for raw_activity in raw_activities:
        activity = json.dumps({
            "Activityid" : raw_activity[0],
            "Name" : raw_activity[1],
            "Type" : raw_activity[2],
            "Location" : raw_activity[3],
            "Price" : raw_activity[4],
            "Price Category" : raw_activity[5],
            "Image" : raw_activity[6],
            "Description" : raw_activity[7]
        })
        output.append(activity)
    
    #Close connection
    conn.close()
    
    return output
    


def internal_get_activities_by_price_category(category : str) -> list:
    """
    Function that retrieves all activities of requested price category.

    Args:
        category (str): One of these categories -> [
            'Free', 
            '$', 
            '$$', 
            '$$$', 
            ]

    Returns:
        list: Each element is a JSON containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve activity
    raw_activities = conn.execute("SELECT * FROM Activities WHERE Price_Category = ?;", (category,)).fetchall()

    #Format activity into JSON format
    output = []
    for raw_activity in raw_activities:
        activity = json.dumps({
            "Activityid" : raw_activity[0],
            "Name" : raw_activity[1],
            "Type" : raw_activity[2],
            "Location" : raw_activity[3],
            "Price" : raw_activity[4],
            "Price Category" : raw_activity[5],
            "Image" : raw_activity[6],
            "Description" : raw_activity[7]
        })
        output.append(activity)
    
    #Close connection
    conn.close()
    
    return output



def internal_get_activities_by_type_and_price_category(type : str, category : str) -> list:
    """
    Function that retrieves all activities of requested type and category.

    Args:
        type (str): One of these types -> [
            'Cultural & Heritage', 
            'Fitness & Wellness', 
            'Food & Beverage', 
            'Outdoor & Nature', 
            'Social & Community Events', 
            'Workshops & Classes'
            ]
            
        category (str): One of these categories -> [
            'Free', 
            '$', 
            '$$', 
            '$$$', 
            ]

    Returns:
        list: Each element is a JSON containing fields Activityid, Name, Type, Location, Price, Price Category, Image and Description. Identifier is Activityid
    """
    #Create connection
    conn = sqlite3.connect("test.db")
    
    #Retrieve activity
    raw_activities = conn.execute("SELECT * FROM Activities WHERE Type = ? AND Price_Category = ?;", (type, category)).fetchall()

    #Format activity into JSON format
    output = []
    for raw_activity in raw_activities:
        activity = json.dumps({
            "Activityid" : raw_activity[0],
            "Name" : raw_activity[1],
            "Type" : raw_activity[2],
            "Location" : raw_activity[3],
            "Price" : raw_activity[4],
            "Price Category" : raw_activity[5],
            "Image" : raw_activity[6],
            "Description" : raw_activity[7]
        })
        output.append(activity)
    
    #Close connection
    conn.close()
    
    return output