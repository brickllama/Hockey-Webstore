from flask import Flask, render_template, session, request, redirect, url_for
from data import Data
import hashlib
import database as db

# app stuff
app = Flask(__name__)
app.secret_key = 'pineapple'


@app.route('/', methods=['GET'])
def home():
    if Data.email == '':
        return redirect(url_for('registration'))
    return render_template("index.html", username=Data.username)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        Data.first_name = request.form.get('first name')
        Data.last_name = request.form.get('last name')
        Data.username = request.form.get('username')
        Data.email = request.form.get('email')
        Data.password = request.form.get('password')
        Data.confirmation = request.form.get('confirmation')
        email = Data.email.lower()
        db.mycursor.execute("SELECT * FROM CUSTOMER WHERE EMAIL=%s", (email,))
        checkUsername = db.mycursor.fetchone()
        if Data.password != Data.confirmation or checkUsername:
            error = "The email provided is already registered."
            return render_template("registration.html", error=error)
        else:
            to_database()
            return redirect(url_for('home'))
    return render_template("registration.html")


@app.route('/account_details')
def account_details():
    return render_template(
        "accountdetails.html",
        first_name=Data.first_name,
        last_name=Data.last_name,
        username=Data.username,
        email=Data.email,
        )


@app.route('/signout')
def signout():
    Data.first_name = ''
    Data.last_name = ''
    Data.username = ''
    Data.email = ''
    Data.password = ''
    Data.confirmation = ''
    return (Data.first_name, Data.last_name, Data.username, Data.email, Data.password, Data.confirmation)


@app.route('/login')
def login():
    return render_template("login.html")


def to_database():
    global Data
    password_bytes = Data.password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    password_hash = hash_object.hexdigest()
    sql = "INSERT INTO CUSTOMER (FIRST_NAME, LAST_NAME, USERNAME, EMAIL, PASSWORD, CONFIRMATION) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (Data.first_name, Data.last_name, Data.username, Data.email, password_hash, password_hash)
    return db.mycursor.execute(sql, val), db.mydb.commit()


if __name__ == '__main__':
    app.run(debug=True)
