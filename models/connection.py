import os
import mariadb

global con
con = None

def create_connection():
    return mariadb.connect(
        host=os.environ["DATABASE_URL"],
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASS"],
        database=os.environ["DATABASE_NAME"]
    )


 
def get_connection():    
    global con
    if con is None:
        con = create_connection()

    try:
        con.ping()
        return con
    except:
        con.close()
        con = create_connection()
        return con
