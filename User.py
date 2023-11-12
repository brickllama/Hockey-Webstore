import hashlib

class User:
    def __init__(self, db, username):
        self.db = db
        self.db.mycursor.execute("SELECT USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PASSWORD FROM CUSTOMER WHERE USERNAME=%s", (username,))
        result = self.db.mycursor.fetchone()
        if result is None:
          raise ValueError
        (self.username, self.first_name, self.last_name, self.email, self.password) = result

    def login(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.password

    @staticmethod
    def register(db, form):
        if form['password'] != form['confirmation']:
            raise ValueError("Passwords don't match")

        db.mycursor.execute("SELECT USERNAME FROM CUSTOMER WHERE USERNAME=%s", (form['username'],))
        if db.mycursor.fetchone():
            raise ValueError('Username is already registered')

        db.mycursor.execute("SELECT EMAIL FROM CUSTOMER WHERE EMAIL=%s", (form['email'],))
        if db.mycursor.fetchone():
            raise ValueError('Email is already registered')

        password_bytes = form['password'].encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        password_hash = hash_object.hexdigest()
        sql = "INSERT INTO CUSTOMER (FIRST_NAME, LAST_NAME, USERNAME, EMAIL, PASSWORD) VALUES (%s, %s, %s, %s, %s)"
        val = (form['first name'], form['last name'], form['username'], form['email'], password_hash)
        return db.mycursor.execute(sql, val), db.mydb.commit()
