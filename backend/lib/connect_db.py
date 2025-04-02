import psycopg2

def connect_db():
    """
        Function that connections to the db and returns a connection
    """
    
    connection = psycopg2.connect(user = "",
                                password = "",
                                host = "",
                                port = "5432",
                                database = "")