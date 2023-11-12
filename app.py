from flask import Flask, render_template, session, request, redirect, url_for
import database as db
from User import User

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
        try:
            User.register(db, request.form)
            session['username'] = request.form['username']
        except Exception as error:
            return render_template("registration.html", error=error)
        return redirect(url_for('home'))
    return render_template("registration.html")


@app.route('/account_details')
def account_details():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        user = User(db, session['username'])
    return render_template(
        "accountdetails.html",
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        )


@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = User(db, request.form['username'])
        except:
            error = "Username or password may be incorrect"
            return render_template("login.html", error=error)

        if user.login(request.form['password']):
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            error = "Username or password may be incorrect"
            return render_template("login.html", error=error)
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
