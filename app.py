from flask import *
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
Bootstrap(app)

app.secret_key = "apT7BsaQ"

# https://www.phpmyadmin.co/db_structure.php?db=sql6490620
# Configuring Database
# app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'jobportal'
mysql = MySQL(app)


@app.route("/")
def homepage():
    if "user" in session:
        return render_template("home.html")
    return redirect("/signin")


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # getting info from signin form
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM jobseeker WHERE (email, password) = (%s, %s) ", (email, password))
        userDetails = cur.fetchone()
        cur.close()
        if not userDetails:
            flash("Invalid Credentials", "danger")
            return redirect(request.url)
        else:
            session['loggedin'] = True
            session["user"] = userDetails[1]
            session['email'] = request.form['email']
            print(userDetails)
            return redirect('/')
    return render_template('signin.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT email FROM jobseeker WHERE email = \"{}\"".format(email))
        duplicateEmail = cur.fetchone()
        cur.close()
        if duplicateEmail:
            flash("Email already exists", "warning")
            return redirect(request.url)
        if(len(phone_number) != 10):
            flash("Phone Number must be only 10 digits long", "warning")
            return redirect(request.url)
        if(not phone_number.isnumeric()):
            flash("Enter only digits [0-9]", "warning")
            return redirect(request.url)
        if password == confirm_password:
            if(len(password) < 8):
                flash("Password field should have at least 8 digits", "warning")
                return redirect(request.url)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO jobseeker(first_name, last_name, phone_number, email, password) VALUES (%s, %s, %s, %s, %s)",
                        (first_name, last_name, phone_number, email, password))
            mysql.connection.commit()
            cur.close()
            session['loggedin'] = True
            session["user"] = request.form['first_name']
            session['email'] = request.form['email']
            return redirect('/manageprofile')
        else:
            message = "Password does not match with Confirm Password"
            flash(message, "warning")
            return redirect(request.url)
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop("user", None)
    session['loggedin'] = False
    return redirect(url_for("signin"))


@app.route("/profile")
def profile():
    if "user" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
            session['email']))
        jobseeker_id = cur.fetchone()
        cur.execute(
            "SELECT job.job_title, job.job_type, company.name, company.location, job.job_salary, job.job_id FROM job INNER JOIN company ON job.company_id = company.company_id WHERE job.job_id in (SELECT job_id FROM apply WHERE jobseeker_id=" + str(jobseeker_id[0]) + ")")
        applied_jobs = cur.fetchall()
        cur.execute("SELECT * FROM profile WHERE jobseeker_id=" +
                    str(jobseeker_id[0]))
        profile_details = cur.fetchone()
        cur.close()
        return render_template('profile.html', profile=profile_details, applied_jobs=applied_jobs)
    else:
        return redirect(url_for('signin'))


@app.route("/manageprofile", methods=["GET", "POST"])
def manageProfile():
    if "user" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
            session['email']))
        jobseeker_id = cur.fetchone()
        cur.execute("SELECT * FROM profile WHERE jobseeker_id=" +
                    str(jobseeker_id[0]))
        profile_data = cur.fetchone()
        print(profile_data)
        cur.close()
        if request.method == 'POST':
            college = request.form['college']
            dept = request.form['dept']
            education = request.form['education']
            resume = request.files['resume']
            filename = resume.filename
            cur = mysql.connection.cursor()
            if profile_data:
                if filename:
                    customeFileName = str(jobseeker_id[0]) + "_" + filename
                    path = os.path.join(r"./static", customeFileName)
                    with open(path, 'wb') as file:
                        file.write(resume.read())
                query = "UPDATE profile SET college = \"{}\", department = \"{}\", education = \"{}\", resume=\"{}\" WHERE jobseeker_id=".format(
                    college, dept, education, filename) + str(jobseeker_id[0])
                cur.execute(query)
                mysql.connection.commit()
            else:
                if filename:
                    customeFileName = str(jobseeker_id[0]) + "_" + filename
                    path = os.path.join(r"./static", customeFileName)
                    with open(path, 'wb') as file:
                        file.write(resume.read())
                cur.execute(
                    f"INSERT INTO profile(college, department, education, resume, jobseeker_id) VALUES (\"{college}\", \"{dept}\", \"{education}\", \"{filename}\"," + str(jobseeker_id[0]) + ")")
                mysql.connection.commit()
            cur.close()
            return redirect(url_for('profile'))
        return render_template('manageprofile.html', profile=profile_data)
    else:
        return redirect(url_for('signin'))


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    if "user" in session:
        if request.method == 'POST':
            keyword = request.form['keywords']
            location = request.form['location']
            cur = mysql.connection.cursor()
            if keyword and (not location):
                cur.execute("SELECT job.job_title, job.job_type, company.name, company.location, job.job_salary, job.job_description, job.job_id FROM job INNER JOIN company ON job.company_id = company.company_id WHERE company.name LIKE \"%{}%\" OR job.job_title LIKE \"%{}%\" OR job.job_type LIKE \"%{}%\" OR job.job_description LIKE \"%{}%\"".format(keyword, keyword, keyword, keyword))
            elif location and (not keyword):
                cur.execute("SELECT job.job_title, job.job_type, company.name, company.location, job.job_salary, job.job_description, job.job_id FROM job INNER JOIN company ON job.company_id = company.company_id WHERE company.location LIKE \"%{}%\"".format(location))
            elif location and keyword:
                cur.execute("SELECT job.job_title, job.job_type, company.name, company.location, job.job_salary, job.job_description, job.job_id FROM job INNER JOIN company ON job.company_id = company.company_id WHERE company.name LIKE \"%{}%\" OR job.job_title LIKE \"%{}%\" OR job.job_type LIKE \"%{}%\" OR job.job_description LIKE \"%{}%\" AND company.location LIKE \"%{}%\"".format(keyword, keyword, keyword, keyword, location))
            jobsearch = cur.fetchall()
            print(jobsearch)
            cur.close()
            return render_template('jobsearch.html', searchResult=jobsearch)
        cur = mysql.connection.cursor()
        cur.execute("SELECT job.job_title, job.job_type, company.name, company.location, job.job_salary, job.job_description, job.job_id FROM job INNER JOIN company ON job.company_id = company.company_id")
        alljobs = cur.fetchall()
        # print(alljobs);
        if len(alljobs) > 0:
            return render_template('jobs.html', jobs=alljobs)
    else:
        return redirect(url_for('signin'))


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if "user" in session:
        if request.method == 'POST':
            job_id = request.form['job_id']
            cur = mysql.connection.cursor()
            cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
                session['email']))
            jobseeker_id = cur.fetchone()
            cur.execute(
                "SELECT * FROM apply WHERE (jobseeker_id, job_id) = (\"{}\", \"{}\")".format(str(jobseeker_id[0]), job_id))
            applied = cur.fetchall()
            if len(applied) == 0:
                cur.execute("INSERT INTO apply VALUES (\"{}\", \"{}\")".format(
                    str(jobseeker_id[0]), job_id))
                mysql.connection.commit()
            cur.close()
        return redirect("/")
    else:
        return redirect(url_for('signin'))


@app.route("/interviews")
def interview():
    if "user" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
            session['email']))
        jobseeker_id = cur.fetchone()
        cur.execute(
            "SELECT * FROM apply INNER JOIN interview ON (apply.jobseeker_id, apply.job_id) = (interview.jobseeker_id, interview.job_id) WHERE interview.jobseeker_id=" + str(jobseeker_id[0]))
        check_apply = cur.fetchall()
        if len(check_apply) > 0:
            cur.execute("SELECT interview.jobseeker_id, job.job_title, company.name, interview.date, interview.time FROM job INNER JOIN company ON job.company_id = company.company_id INNER JOIN interview ON interview.job_id = job.job_id WHERE interview.jobseeker_id=" +
                        str(jobseeker_id[0]) + " AND interview.job_id IN (SELECT apply.job_id FROM apply INNER JOIN interview ON (apply.jobseeker_id, apply.job_id) = (interview.jobseeker_id, interview.job_id) WHERE interview.jobseeker_id=" + str(jobseeker_id[0]) + ")")
            interviews = cur.fetchall()
        else:
            interviews = None
        return render_template('interviews.html', interviews=interviews)
    else:
        return redirect(url_for('signin'))


@app.route("/results")
def results():
    if "user" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
            session['email']))
        jobseeker_id = cur.fetchone()
        cur.execute(
            'SELECT * FROM apply INNER JOIN result ON (apply.jobseeker_id, apply.job_id) = (result.jobseeker_id, result.job_id) WHERE result.jobseeker_id=' + str(jobseeker_id[0]))
        chk_apply = cur.fetchall()
        if len(chk_apply) > 0:
            cur.execute("SELECT result.jobseeker_id, job.job_title, company.name, company.location, result.status FROM \
			job INNER JOIN company ON job.company_id = company.company_id INNER JOIN result ON result.job_id = job.job_id WHERE result.jobseeker_id = " + str(jobseeker_id[0]) + " AND result.job_id IN (SELECT apply.job_id FROM apply INNER JOIN result ON (apply.jobseeker_id, apply.job_id) = (result.jobseeker_id, result.job_id) WHERE result.jobseeker_id = " + str(jobseeker_id[0]) + ");")
            res = cur.fetchall()
            if len(res) == 0:
                res = None
        else:
            res = None
        return render_template('results.html', res=res)
    else:
        return redirect(url_for('signin'))


@app.route("/account", methods=["GET", "POST"])
def account():
    if "user" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
            session['email']))
        jobseeker_id = cur.fetchone()
        cur.execute(
            "SELECT * FROM jobseeker WHERE jobseeker_id = " + str(jobseeker_id[0]))
        account = cur.fetchone()
        return render_template("account.html", account=account)
    else:
        return redirect(url_for("signin"))


@app.route("/accountSummary")
def accountSummary():
    if "user" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
            session['email']))
        jobseeker_id = cur.fetchone()
        cur.execute(
            'SELECT count(job_id) FROM apply GROUP BY jobseeker_id HAVING jobseeker_id  = ' + str(jobseeker_id[0]))
        applied = cur.fetchone()
        cur.execute(
            'SELECT count(job_id) FROM result GROUP BY jobseeker_id HAVING jobseeker_id = ' + str(jobseeker_id[0]))
        results = cur.fetchone()
        cur.execute(
            'SELECT count(job_id) FROM interview GROUP BY jobseeker_id HAVING jobseeker_id = ' + str(jobseeker_id[0]))
        interviews = cur.fetchone()
        return render_template('accountSummary.html', applied=applied, results=results, interviews=interviews)
    else:
        return redirect(url_for("signin"))


@app.route("/changePassword", methods=["GET", "POST"])
def changePassword():
    if "user" in session:
        if request.method == "POST":
            password = request.form['password']
            cpassword = request.form['cpassword']
            if password == cpassword:
                if(len(password) < 8):
                    flash("Password field should have at least 8 digits", "warning")
                    return redirect(request.url)
            else:
                message = "Password does not match with Confirm Password"
                flash(message, "warning")
                return redirect(request.url)
            cur = mysql.connection.cursor()
            cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
                session['email']))
            jobseeker_id = cur.fetchone()
            cur.execute(
                f"UPDATE jobseeker SET password = \"{password}\" WHERE jobseeker_id = " + str(jobseeker_id[0]))
            mysql.connection.commit()
            cur.close()
            return redirect("/account")
        return render_template("changePassword.html")
    return redirect("/signin")


@app.route("/editAccount", methods=["GET", "POST"])
def editAccount():
    if "user" in session:
        if request.method == "GET":
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM jobseeker WHERE email = \"{}\"".format(session['email']))
            jobseeker = cur.fetchone()
            cur.close()
            return render_template("editAccount.html", details=jobseeker)
        elif request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone_number = request.form['phone_number']
            email = request.form['email']
            cur = mysql.connection.cursor()
            cur.execute("SELECT jobseeker_id FROM jobseeker WHERE email = \"{}\"".format(
                session['email']))
            jobseeker_id = cur.fetchone()
            cur.execute(
                "SELECT email FROM jobseeker WHERE email = \"{}\"".format(email))
            duplicateEmail = cur.fetchone()
            if duplicateEmail:
                flash("Email already exists", "warning")
                return redirect(request.url)
            if(len(phone_number) != 10):
                flash("Phone Number must be only 10 digits long", "warning")
                return redirect(request.url)
            if(not phone_number.isnumeric()):
                flash("Enter only digits [0-9]", "warning")
                return redirect(request.url)
            cur.execute(
                f"UPDATE jobseeker SET first_name = \"{first_name}\", last_name = \"{last_name}\", phone_number = {phone_number}, email = \"{email}\" WHERE jobseeker_id = " + str(jobseeker_id[0]))
            mysql.connection.commit()
            session['email'] = email
            cur.close()
            return redirect("/account")
    return redirect("/")


@app.route("/addCompany", methods=["GET", "POST"])
def addCompany():
    if "user" in session and session["email"] == "admin@hireit.com":
        if request.method == "POST":
            name = request.form['name']
            location = request.form['location']
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT name FROM company where name = \"{name}\"")
            exists = cur.fetchone()
            if exists:
                flash("Company already exists in database", "warning")
                return redirect(request.url)
            cur.execute(
                f"INSERT INTO company (name, location) VALUE (\"{name}\", \"{location}\")")
            mysql.connection.commit()
            cur.close()
            flash("Company details added to database", "success")
            return redirect("/")
        return render_template("addCompany.html")
    flash("Sign In as Admin", "warning")
    return redirect("/signin")


@app.route("/addJob", methods=["GET", "POST"])
def addjob():
    print(session['email'])
    if "user" in session and session["email"] == "admin@hireit.com":
        if request.method == "POST":
            company_name = request.form['company_name']
            job_title = request.form['job_title']
            job_type = request.form['job_type']
            job_description = request.form['job_description']
            salary = request.form['salary']
            cur = mysql.connection.cursor()
            cur.execute(
                f"SELECT company_id FROM company where name LIKE \"%{company_name}%\"")
            company_id = cur.fetchone()
            if company_id != None:
                company_id = company_id[0]
            if not company_id:
                flash("Add company before inserting job", "danger")
                return redirect("/addCompany")
            cur.execute(
                f"INSERT INTO job (job_title, job_type, job_description, job_salary, company_id) VALUES (\"{job_title}\", \"{job_type}\", \"{job_description}\", {salary}, {company_id})")
            mysql.connection.commit()
            cur.close()
            flash("Job added to database", "success")
            return redirect("/")
        return render_template("insertJob.html")
    flash("Sign In as Admin", "warning")
    return redirect("/signin")


@app.route("/scheduleInterview", methods=["GET", "POST"])
def scheduleInterview():
    if "user" in session and session["email"] == "admin@hireit.com":
        if request.method == "POST":
            company_name = request.form['company_name']
            job_title = request.form['job_title']
            date = request.form['date']
            time = request.form['time']
            candidate_email = request.form['email']
            cur = mysql.connection.cursor()
            cur.execute(
                f"SELECT company_id FROM company where name LIKE \"%{company_name}%\"")
            company_id = cur.fetchone()
            if company_id != None:
                company_id = company_id[0]
            if not company_id:
                flash("Add Company before inserting job", "danger")
                return redirect("/addCompany")
            cur.execute("SELECT job_id FROM job where company_id =" +
                        str(company_id) + f" AND job_title = \"{job_title}\"")
            job_id = cur.fetchone()
            if job_id != None:
                job_id = job_id[0]
            if not job_id:
                flash("Add Job before scheduling interview", "danger")
                return redirect("/addJob")
            cur.execute(
                f"SELECT jobseeker_id FROM jobseeker where email LIKE \"{candidate_email}\"")
            jobseeker_id = cur.fetchone()
            if jobseeker_id != None:
                jobseeker_id = jobseeker_id[0]
            if not jobseeker_id:
                flash("User does not exist", "danger")
                return redirect("/")
            cur.execute(
                f"INSERT INTO interview (job_id, date, time, jobseeker_id) VALUES ({job_id}, \"{date}\", \"{time}\", {jobseeker_id})")
            mysql.connection.commit()
            cur.close()
            flash("Done !! Scheduled Interview ", "success")
            return redirect("/")
        return render_template("scheduleInterview.html")
    flash("Sign In as Admin", "warning")
    return redirect("/signin")


@app.route("/declareResult", methods=["GET", "POST"])
def declareResult():
    if "user" in session and session["email"] == "admin@hireit.com":
        if request.method == "POST":
            company_name = request.form['company_name']
            job_title = request.form['job_title']
            candidate_email = request.form['email']
            status = request.form['status']
            cur = mysql.connection.cursor()
            cur.execute(
                f"SELECT company_id FROM company where name LIKE \"%{company_name}%\"")
            company_id = cur.fetchone()
            if company_id != None:
                company_id = company_id[0]
            if not company_id:
                flash("Add Company before inserting job", "danger")
                return redirect("/addCompany")
            cur.execute("SELECT job_id FROM job where company_id =" +
                        str(company_id) + f" AND job_title = \"{job_title}\"")
            job_id = cur.fetchone()
            if job_id != None:
                job_id = job_id[0]
            if not job_id:
                flash("Job does not exist !", "danger")
                return redirect("/addJob")
            cur.execute(
                f"SELECT jobseeker_id FROM jobseeker where email LIKE \"{candidate_email}\"")
            jobseeker_id = cur.fetchone()
            if jobseeker_id != None:
                jobseeker_id = jobseeker_id[0]
            if not jobseeker_id:
                flash("User does not exist", "danger")
                return redirect("/")
            cur.execute(
                f"INSERT INTO result (jobseeker_id, job_id, status) VALUES ({jobseeker_id}, {job_id}, {int(status)})")
            mysql.connection.commit()
            cur.close()
            return redirect("/")
        return render_template("declareResult.html")
    flash("Sign In as Admin", "warning")
    return redirect("/signin")


if (__name__ == "__main__"):
    app.run(debug=True, host="localhost")
