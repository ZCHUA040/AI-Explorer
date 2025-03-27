import sqlite3, json


def get_all_activities() -> list:
    """
    Function that retreives all activites in Activities Table

    Returns:
        list: Each element is a JSON containing fields Activityid, Name, Type, Location and Price. Identifier is Activityid
    """
    
    #Get Connection
    conn = sqlite3.connect("../test.db")
    
    #Retrieves activities   
    activites = conn.execute("SELECT * FROM Activities;")
    
    #Format the output in proper format
    output = []
    for activity in activites:
        element = json.dumps({
            "Activityid" : activity[0],
            "Name" : activity[1],
            "Type" : activity[2],
            "Location" : activity[3],
            "Price" : activity[4]
        })
        output.append(element)
        
    #Close connection
    conn.close()
    
    return output



def get_activity_by_id(int : id) -> str:
    """
    Function that returns a single activity based on the activity id.

    Args:
        int (id): Activityid of the activity that is being requested

    Returns:
        str: JSON containing fields Activityid, Name, Type, Location and Price. Identifier is Activityid
    """
    
    #Create connection
    conn = sqlite3.connect("../test.db")
    
    #Retrieve activity
    raw_activity = conn.execute("SELECT * FROM Activities WHERE Activityid = ?;", id)

    #Format activity into JSON format
    activity = json.dumps({
        "Activityid" : raw_activity[0],
        "Name" : raw_activity[1],
        "Type" : raw_activity[2],
        "Location" : raw_activity[3],
        "Price" : raw_activity[4]
    })
    
    #Close connection
    conn.close()
    
    return activity

