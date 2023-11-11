import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3006",
    user="root",
    password="demo",
    database="testdatabase"
)

mycursor = mydb.cursor()
