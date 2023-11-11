from flask import Flask, render_template, session, request, redirect, url_for
import hashlib
import database as db

# app stuff
app = Flask(__name__)
app.secret_key = 'pineapple'


@app.route('/', methods=['GET'])
def home():
    if 'username' not in session:
        return redirect(url_for('registration'))
    return render_template("index.html", username=session['username'])


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        session['first_name'] = request.form['first name']
        session['last_name'] = request.form['last name']
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        session['confirmation'] = request.form['confirmation']
        email = session['email']
        db.mycursor.execute("SELECT * FROM CUSTOMER WHERE EMAIL=%s", (email,))
        checkEmail = db.mycursor.fetchone()
        if session['password'] != session['confirmation'] or checkEmail:
            error = "The email provided is already registered."
            return render_template("registration.html", error=error)
        else:
            to_database()
            return redirect(url_for('home'))
    return render_template("registration.html")


@app.route('/account_details')
def account_details():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        username = session['username']
        db.mycursor.execute("SELECT FIRST_NAME, LAST_NAME, USERNAME, EMAIL FROM CUSTOMER WHERE USERNAME=%s", (username,))
        result = db.mycursor.fetchall()
        for row in result:
            session['first_name'] = row[0]
            session['last_name'] = row[1]
            session['username'] = row[2]
            session['email'] = row[3]
    return render_template(
        "accountdetails.html",
        first_name=session['first_name'],
        last_name=session['last_name'],
        username=session['username'],
        email=session['email'],
        )


@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        db.mycursor.execute("SELECT PASSWORD FROM CUSTOMER WHERE USERNAME=%s", (session['username'],))
        checkPassword = db.mycursor.fetchone()
        if checkPassword is not None and hashlib.sha256(session['password'].encode()).hexdigest() == checkPassword[0]:
            return redirect(url_for('home'))
        else:
            error = "Username or password may be incorrect"
            session.pop('password', None)
            return render_template("login.html", error=error)
    return render_template("login.html")


def to_database():
    password_bytes = session['password'].encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    password_hash = hash_object.hexdigest()
    sql = "INSERT INTO CUSTOMER (FIRST_NAME, LAST_NAME, USERNAME, EMAIL, PASSWORD, CONFIRMATION) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (session['first_name'], session['last_name'], session['username'], session['email'], password_hash, password_hash)
    return db.mycursor.execute(sql, val), db.mydb.commit()


if __name__ == '__main__':
    app.run(debug=True)
