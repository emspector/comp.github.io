import os
import datetime
import logging

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import requests
import urllib.parse
from functools import wraps

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True    

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///comp.db")

# register(): allow users to make profiles on the site; the password is set to a default in order to make sure that not just anyone can make a useable account on the site
# anyone can make an account but they won't be able to access it unless they are informed of the default password (which they can then change after logging in)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # get the inputted name
        name = request.form.get("name")
        if not name:
            return apology("name required", 403)

         # get the inputted pronouns
        pronouns = request.form.get("pronouns")
        if not pronouns:
            return apology("pronouns required", 403)

        # get the inputted phone number
        phone = request.form.get("phone")
        if not phone:
            return apology("phone number required", 403)

        # get the inputted dorm/house
        dorm = request.form.get("dorm")
        if not dorm:
            return apology("dorm/house required", 403)

        # get the inputted room number + entryway
        room = request.form.get("room")
        if not room:
            return apology("entryway + room required", 403)

        # get the inputted email address
        email = request.form.get("email")
        if not email:
            return apology("email required", 403)
        # make sure the email is different from one already in the system
        existing_emails = db.execute("SELECT email FROM profiles WHERE email=:email", email=email)
        if existing_emails:
            return apology("email already in database", 403)

        # make sure the email and email confirmation match
        email_confirm = request.form.get("email_confirm")
        if not email_confirm:
            return apology("email confirmation required", 403)
        if email != email_confirm:
            return apology("email must match confirmation", 403)

        # set default password
        password = "herbiewhrbie953"

        # get the password hash
        pass_hash = generate_password_hash(password)

        # input all gathered information into the profiles table
        db.execute("INSERT INTO profiles (name, pronouns, phone, email, dorm, room, password) VALUES (:name, :pronouns, :phone, :email, :dorm, :room, :pass_hash)", name=name, pronouns=pronouns, phone=phone, email=email, dorm=dorm, room=room, pass_hash=pass_hash)
        session["email"] = "email"

        return redirect("/")

# simple login, borrowed from CS50 Finance
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM profiles WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# index() pull content from SQL database to populate the user's dashboard homepage
@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    # pull the user's name from the profile table
    name = db.execute("SELECT name FROM profiles WHERE user_id=:user_id", user_id=user_id)[0]["name"]

    # pull attendance records from the attendance table
    att_table = db.execute("SELECT meeting_num FROM attendance WHERE user_id=:user_id", user_id=user_id)

    # pull assignment submission records the assignments table
    sub_table = db.execute("SELECT assignment, submission FROM assignments WHERE user_id=:user_id", user_id=user_id)

    return render_template("index.html", att_table=att_table, sub_table=sub_table, name=name)

# about(): this is a simple page with text describing the comp and the site's functionality for compers
@app.route("/about")
@login_required
def about():
    user_id=session["user_id"]

    #get the user's name to display on the page
    name = db.execute("SELECT name FROM profiles WHERE user_id=:user_id", user_id=user_id)[0]["name"]

    return render_template("about.html", name=name)

# attendance(): allow the user to mark themselves present at comp meetings and office hours
@app.route("/attendance", methods=["GET", "POST"])
@login_required
def attendance():
    if request.method == "GET":
        user_id = session["user_id"]

        # pull the user's name from the profiles table
        name = db.execute("SELECT name FROM profiles WHERE user_id=:user_id", user_id=user_id)[0]["name"]

        # pull attendance records from the attendance table
        att_table = db.execute("SELECT meeting_num FROM attendance WHERE user_id=:user_id", user_id=user_id)

        return render_template("attendance.html", att_table=att_table, name=name)

    else: #user can log attendance at meetings and office hours

        # make sure list option is selected
        if request.form.get("att_list"):

            user_id = session["user_id"]

            # pull event name to be marked present at
            meeting_num = request.form.get("att_list")

            # pull all previous attendance records for user
            attendance = db.execute("SELECT meeting_num FROM attendance WHERE user_id=:user_id", user_id=user_id)

            # make sure the user doesn't accidentally mark themselves present at the same event twice
            for row in attendance:
                if row["meeting_num"] == meeting_num:
                    return redirect("/attendance")

            # having made sure the user has never marked themself present at this event before, insert the new attendance record
            db.execute("INSERT INTO attendance (user_id, meeting_num) VALUES (:user_id, :meeting_num)",
                           user_id=user_id, meeting_num=meeting_num)

            return redirect("/attendance")

        else: # if the user did not pick an event from the list

            return redirect("/attendance")

# assignments(): present a list of assignments and a link to the submission protal
@app.route("/assignments")
@login_required
def assignments():
    if request.method == "GET":
        user_id = session["user_id"]

        # get the user's name from the profiles for display on the page
        name = db.execute("SELECT name FROM profiles WHERE user_id=:user_id", user_id=user_id)[0]["name"]

        return render_template("assignments.html", name=name)

# submit(): allow the user to submit a link to their comp assignment, so the comp directors can evaluate it
@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    if request.method == "GET":
        user_id = session["user_id"]


        # get the user's name from the profiles table for display on the page
        name = db.execute("SELECT name FROM profiles WHERE user_id=:user_id", user_id=user_id)[0]["name"]

        # pull submission records so as to populate the submission log
        sub_table = db.execute("SELECT assignment, submission FROM assignments WHERE user_id=:user_id", user_id=user_id)

        return render_template("submit.html", sub_table=sub_table, name=name)

    else: # method == post, user is submitting an assignment and the link must be added to the assignments table

        # make sure an assignment was chosen from the list and that a link was entered
        if request.form.get("sub_list") and request.form.get("link_input"):

            user_id = session["user_id"]

            # pull the assignment from the list to indicate which assignment the user is submitting
            assign_num = request.form.get("sub_list")

            # get the link from the input field
            link_input = request.form.get("link_input")

            # if the user is submitting a link for an assignment they already submitted, replace the original link in the assignments table with the newly submitted one
            submissions = db.execute("SELECT assignment FROM assignments WHERE user_id=:user_id", user_id=user_id)
            for row in submissions:
                if row["assignment"] == assign_num:
                    db.execute("UPDATE assignments SET submission = :link_input WHERE assignment=:assign_num", link_input=link_input, assign_num=assign_num)
                    return redirect("/submit")

            # if they are submitting an assignment for the first time, insert the link into the assignments table
            db.execute("INSERT INTO assignments (user_id, assignment, submission) VALUES (:user_id, :assign_num, :link_input)",
                           user_id=user_id, assign_num=assign_num, link_input=link_input)

            return redirect("/submit")

        else: # if the user did not select an assignment and input a link

            return redirect("/submit")

# people(): a directory of the people involved in the comp
@app.route("/people")
@login_required
def people():
    user_id = session["user_id"]

    #get the user's name from the profiles table for display on the page
    name = db.execute("SELECT name FROM profiles WHERE user_id=:user_id", user_id=user_id)[0]["name"]

    # gather information from the profiles table in alphabetical order
    prof_table = db.execute("SELECT * FROM profiles ORDER BY name ASC")

    return render_template("people.html", prof_table=prof_table, name=name)

# admin(): a page accessible only by the comp directors (identified by their email addresses) which allows them to view all profile, attendance, and assignment records, organized by comper
# also includes an automatically created email list, formatted so it can be copied and pasted into an email service as-is
# and includes a list of comper addresses to make the process of organizing the dorm-storm at the end of the comp very easy
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "GET":
        user_id = session["user_id"]

        # create a table of all the emails in the system
        current = db.execute("SELECT email FROM profiles WHERE user_id=:user_id", user_id=user_id)

        # check to see if the user is a director (comp director emails hardcoded)
        if (current[0]["email"] == "emilyspector@college.harvard.edu") or (current[0]["email"] == "broberts@college.harvard.edu") or (current[0]["email"] == "bchemberlin@college.harvard.edu"):

            # pull ALL profile, attendance, and assignment records
            prof_table = db.execute("SELECT * FROM profiles ORDER BY name ASC")
            att_table = db.execute("SELECT * FROM attendance ORDER BY timestamp ASC")
            sub_table = db.execute("SELECT * FROM assignments ORDER BY timestamp ASC")

            # identify user's name for display on the page
            name = db.execute("SELECT name FROM profiles WHERE user_id=:user_id", user_id=user_id)[0]["name"]

            return render_template("admin.html", att_table=att_table, sub_table=sub_table, prof_table=prof_table, name=name)

        else: #return an apology if the user attempting to access the admin page is not a comp director
            return apology("this page is for comp directors only", 403)

    else: # allow comp-directors to assign a "grade" to comper assignments if they have not yet been marked

        # pull the evaluation text from the input form
        evaluation = request.form.get("evaluation")

        # pull the assignment submission id (unique)
        sub_id = request.form.get("sub_id")

        # change the evaluation field in the assignments table to the newly submitted evaluation from its default value of "TODO"
        db.execute("UPDATE assignments SET evaluation = :evaluation WHERE sub_id=:sub_id", evaluation=evaluation, sub_id=sub_id)

        return redirect("/admin")

# drop(): allow comp directors to remove the students who have dropped out of the comp so the interface doesn't get noisy with profiles that are out of use
# email addresses are ascertained to be unique in the register functions, so deletion is executed by email address
@app.route("/drop", methods=["POST"])
@login_required
def drop():
    # pull the email address enterred in the form
    email = request.form.get("email")

    # find the user_id of the comper to be deleted, so their information can be accessed in all three tables
    drop_id = db.execute("SELECT user_id FROM profiles WHERE email=:email", email=email)
    drop_id = drop_id[0]["user_id"]

    # delete from all three tables
    db.execute("DELETE FROM profiles WHERE user_id=:drop_id", drop_id=drop_id)
    db.execute("DELETE FROM assignments WHERE user_id=:drop_id", drop_id=drop_id)
    db.execute("DELETE FROM attendance WHERE user_id=:drop_id", drop_id=drop_id)
    return redirect("/admin")

# password(): let users change their passwords
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "GET":
        return render_template("password.html")

    else:
        # gather the content enterred in all the fields on the page
        if request.form.get("old_pass") and request.form.get("new_pass") and request.form.get("confirmation"):
            user_id = session["user_id"]
            old_pass = request.form.get("old_pass")
            new_pass = request.form.get("new_pass")
            confirmation = request.form.get("confirmation")

          # Ensure password was submitted
        if not request.form.get("old_pass"):
            return apology("must enter old password", 403)

        # Ensure new password was submitted
        if not request.form.get("new_pass"):
            return apology("must enter new password", 403)

        # Ensure new password confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must confirm new password", 403)

        # pull profile information for the user
        rows = db.execute("SELECT * FROM profiles WHERE user_id = :user_id",
                          user_id=session["user_id"])

        # use same mechanism as login function to make sure the old password is correct
        if not check_password_hash(rows[0]["password"], request.form.get("old_pass")):
            return apology("invalid old password", 403)

        # check that the new password and confirmation fields match
        if new_pass != confirmation:
            return apology("password must match confirmation", 403)

        # generate the hash for the new password
        new_pass = generate_password_hash(new_pass)

        # update the profiles table to reflect the new password for the user
        db.execute("UPDATE profiles SET password = :new_pass WHERE user_id=:user_id", new_pass=new_pass, user_id=session["user_id"])

        return redirect("/")

# simple logout, borrowed from CS50 Finance
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
