import mysql.connector
import os

mydb = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "127.0.0.1"),
    port=os.getenv("MYSQL_PORT", "3006"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASS", "demo"),
    database=os.getenv("MYSQL_DB", "testdatabase")
)

mycursor = mydb.cursor()
