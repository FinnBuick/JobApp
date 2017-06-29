from flask import render_template, flash, redirect, request, url_for, session
from app import app
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from dbconnect import connection
from .forms import JobForm, RegistrationForm
import gc


@app.route('/')
@app.route('/dashboard/')
def dashboard():
    form = RegistrationForm()
    try:
        cursor, conn = connection()
        cursor.execute("SELECT JobID, JobName, ClientName, AccountManager, StartDate FROM job ORDER BY jobID DESC")
        data = list(cursor.fetchall())
    except Exception as e:
        return(str(e))

    return render_template('dashboard.html', data=data, form=form)


@app.route('/addjob/', methods=['GET', 'POST'])
def add_job():
    try:
        cursor, conn = connection()
        cursor.execute("SELECT DISTINCT AccountManager FROM job ORDER BY AccountManager")
        accmanagers = cursor.fetchall()

        cursor.execute("SELECT DISTINCT ClientName FROM job ORDER BY ClientName")
        clients = cursor.fetchall()

        # Converts clients into list of (key, value) pairs
        arr = []
        for el in clients:
            arr.append(el[0])

        clientchoices = [(key, key) for key in arr]

        # Converts accmanagers into list of (key, value) pairs
        arr = []
        for el in accmanagers:
            arr.append(el[0])

        accmanagerchoices = [(key, key) for key in arr]

    except Exception as e:
        return(str(e))

    form = JobForm()
    form.clientname.choices = clientchoices
    form.accountmanager.choices = accmanagerchoices
    return render_template('addjob.html', form=form)

@app.route('/deletejob/', methods=['GET', 'POST'])
def delete_job():
    try:
        cursor, conn = connection()
        cursor.execute("SELECT JobID, JobName, ClientName, AccountManager, StartDate FROM job ORDER BY jobID DESC")
        data = list(cursor.fetchall())
    except Exception as e:
        return(str(e))

    return render_template('deletejob.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def page_not_found(e):
    return render_template('405.html')


@app.route('/login/', methods=['GET', 'POST'])
def login_page():

    error = ""
    try:
        if request.method == 'POST':
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            # flash(attempted_username)
            # flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid credentials. Try Again."

        # flash(attempted_username)
        return render_template('login.html', error=error)


    except Exception as e:
        flash(e)
        return render_template('login.html', error=error)


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == 'POST' and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))
            cursor, conn = connection()

            x = cursor.execute("SELECT * FROM users WHERE username = (%s)",
                               (thwart(username)))

            if int(len(x)) > 0:
                flash("That username is already taken, please try another")
                return render_template("register.html", form=form)
            else:
                cursor.execute("INSERT INTO users (username, passwd, email) VALUES (%s, %s, %s",
                               thwart(username),thwart(password), thwart(email))
                conn.autocommit()
                flash("Thanks for registering!")
                cursor.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return (str(e))
