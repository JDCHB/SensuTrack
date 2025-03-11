import mysql.connector


"""
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mascotas"
    )"""

# MASCOTAS

def get_db_connection():
    return mysql.connector.connect(
        host="brqxd0rfhpuczons9wai-mysql.services.clever-cloud.com",
        user="usroznc53rytwkal",
        password="Io6BgzSFgRU4cp8LNsCT",
        database="brqxd0rfhpuczons9wai"
    )

