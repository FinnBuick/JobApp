import pymysql

def connection():
    conn = pymysql.connect("localhost",
                           "root",
                           "wolfbuick99",
                           "exhibitioncojobs")
    cursor = conn.cursor()

    return cursor, conn