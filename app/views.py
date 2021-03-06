from flask import render_template, flash, redirect, request, url_for, session
from app import app
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from dbconnect import connection
from tsheetsAPI import post_new_job
from .forms import JobForm, RegistrationForm
import datetime
import gc



@app.route('/')
@app.route('/dashboard/')
def dashboard():
    form = RegistrationForm()
    try:
        cursor, conn = connection()
        cursor.execute("SELECT JobID, JobName, ClientName, AMName, StartDate, InstallDate FROM job, accountmanager, client WHERE job.ClientID = client.ClientID AND job.AccountManagerID = accountmanager.AccountManagerID ORDER BY jobID DESC")
        data = list(cursor.fetchall())
    except Exception as e:
        return (str(e))

    return render_template('dashboard.html', data=data, form=form)


@app.route('/addjob/', methods=['GET', 'POST'])
def add_job():

    # Fetch data for drop down selection
    try:
        cursor, conn = connection()
        cursor.execute("SELECT DISTINCT AMName FROM accountmanager ORDER BY AMName;")
        accmanagers = cursor.fetchall()

        cursor.execute("SELECT DISTINCT ClientName FROM client ORDER BY ClientName;")
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
        return (str(e))

    form = JobForm(request.form)
    form.clientnameselect.choices = clientchoices
    form.accountmanager.choices = accmanagerchoices

    clientform = JobForm(request.form)

    # Handle form data and update database
    try:
        cursor, conn = connection()

        if form.validate_on_submit():

            jobname = form.jobname.data
            clientname = form.clientnameselect.data
            startdate = datetime.date.today()
            installdate = form.installdate.data
            accountmanager = form.accountmanager.data


            cursor.execute("INSERT INTO job (JobName, ClientName, StartDate, InstallDate, AccountManager) VALUES (%s, %s, %s, %s, %s);",
                           (thwart(jobname), thwart(clientname), startdate, thwart(installdate.strftime('%Y-%m-%d %H:%M:%S')), thwart(accountmanager)))

            conn.commit()

            #POST new job to TSheets using tsheetsAPI
            cursor.execute("SELECT `JobID` FROM job WHERE `JobName` = '{0}' LIMIT 1".format(jobname))
            jobid = cursor.fetchone()
            jobid = str(jobid[0])
            statuscode = post_new_job(jobid, jobname, clientname)


            cursor.close()
            conn.close()
            gc.collect()

            flash("Job successfully submitted!")
            if statuscode == 200:
                flash("Job successfully added to TSheets")

            return redirect(url_for('dashboard'))
        elif request.method == "POST":
            flash("Job did not submit properly, please make sure you filled out all fields")




    except Exception as e:
        return str(e)

    return render_template('addjob.html', form=form)


@app.route('/addclient/', methods=['POST'])
def add_client():
    client = request.form['clientname']

    try:
        cursor, conn = connection()



    except Exception as e:
        return str(e)

    data = ''
    return redirect(url_for("addjob"))


@app.route('/deletejob/', methods=['GET', 'POST'])
def delete_job():
    # Populate table from database
    try:
        cursor, conn = connection()
        cursor.execute("SELECT JobID, JobName, ClientName, AccountManager, StartDate, InstallDate FROM job ORDER BY jobID DESC")
        data = list(cursor.fetchall())
    except Exception as e:
        return (str(e))

    return render_template('deletejob.html', data=data)


@app.route('/delete', methods=['POST'])
def delete():

    try:
        id = request.form['id']
        cursor, conn = connection()
        cursor.execute("DELETE from job WHERE JobID = {}".format(id))
        conn.commit()
        cursor.close()
        conn.close()
        gc.collect()

        flash("Job deleted successfully!")

    except Exception as e:
        return (str(e))

    return redirect(url_for('delete_job'))


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
                cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s",
                               thwart(username), thwart(password), thwart(email))
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

@app.route("/favicon.ico")
def favicon():
    return(url_for('static',filename='favicon.ico'))

