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
        email = request.form['email']
        username = request.form['username']
        db.mycursor.execute("SELECT EMAIL, USERNAME FROM CUSTOMER WHERE EMAIL=%s OR USERNAME=%s", (email,username))
        results = db.mycursor.fetchone()
        if request.form['password'] != request.form['confirmation']:
            error = "Passwords don't match"
            return render_template("registration.html", error=error)
        elif results:
            error = "The email or username provided is already registered."
            return render_template("registration.html", error=error)
        else:
            session['username'] = results[1]
            to_database(request.form)
            return redirect(url_for('home'))
    return render_template("registration.html")


@app.route('/account_details')
def account_details():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        username = session['username']
        db.mycursor.execute("SELECT USERNAME, FIRST_NAME, LAST_NAME, EMAIL FROM CUSTOMER WHERE USERNAME=%s", (username,))
        result = db.mycursor.fetchall()
        for username, first_name, last_name, email in result:
            pass
    return render_template(
        "accountdetails.html",
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        )


@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db.mycursor.execute("SELECT USERNAME, PASSWORD FROM CUSTOMER WHERE USERNAME=%s", (request.form['username'],))
        results = db.mycursor.fetchone()
        if results and hashlib.sha256(request.form['password'].encode()).hexdigest() == results[1]:
            session['username'] = results[0]
            return redirect(url_for('home'))
        else:
            error = "Username or password may be incorrect"
            session.pop('password', None)
            return render_template("login.html", error=error)
    return render_template("login.html")


def to_database(form):
    password_bytes = form['password'].encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    password_hash = hash_object.hexdigest()
    sql = "INSERT INTO CUSTOMER (FIRST_NAME, LAST_NAME, USERNAME, EMAIL, PASSWORD) VALUES (%s, %s, %s, %s, %s)"
    val = (form['first name'], form['last name'], form['username'], form['email'], password_hash)
    return db.mycursor.execute(sql, val), db.mydb.commit()


if __name__ == '__main__':
    app.run(debug=True)
