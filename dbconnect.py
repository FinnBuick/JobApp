import MySQLdb

def connection():
    conn = MySQLdb.connect("localhost",
                           "root",
                           "wolfbuick99",
                           "mydb")
    cursor = conn.cursor()
    cursor.execute("Use mydb")

    return cursor, conn