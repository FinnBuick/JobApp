import MySQLdb

def connection():
    conn = MySQLdb.connect("localhost",
                           "root",
                           "wolfbuick99",
                           "exhibitioncojobs")
    cursor = conn.cursor()

    return cursor, conn