from flask import render_template, flash, redirect, request, url_for
from app import app
from dbconnect import connection
from .forms import JobForm


@app.route('/')
@app.route('/dashboard/')
def dashboard():
    try:
        cursor, conn = connection()
        cursor.execute("SELECT JobID, JobName, ClientName, AccountManager, StartDate FROM job ORDER BY jobID DESC")
        data = list(cursor.fetchall())
    except Exception as e:
        return(str(e))

    return render_template('dashboard.html', data=data)


@app.route('/addjob/', methods=['GET', 'POST'])
def add_job():
    try:
        cursor, conn = connection()
        cursor.execute("SELECT DISTINCT AccountManager FROM job ORDER BY AccountManager")
        accmanagers = cursor.fetchall()
        flash(accmanagers)

        cursor.execute("SELECT DISTINCT ClientName FROM job ORDER BY ClientName")
        clients = cursor.fetchall()
        it = iter(clients)
        res = zip(it, it)
        flash(res)
    except Exception as e:
        return(str(e))

    form = JobForm()
    form.clientname.choices = res
    return render_template('addjob.html', form=form,  accmanagers=accmanagers)

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

