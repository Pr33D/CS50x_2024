import calendar

from flask import Flask, redirect, render_template as render, request, session, flash, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time

from functions import login_required, insert_user, get_users, get_taskz, insert_task, check_task, delete_task


# config app
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# general pages with no login needed from here
@app.route("/")
def index():
    """ The Apps home page """

    #TODO

    if session["user"]:
        return redirect(url_for("overview"))

    return render("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Page for user registration """

    if request.method == "POST":
        # request form entries
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        errors = False

        # required fields not empty and match
        if not username:
            flash("Please enter a Username")
            errors = True
        if not password:
            flash("Please enter a password")
            errors = True
        if not confirmation:
            flash("Please confirm your password")
            errors = True
        if password != confirmation:
            flash("Passwords do not match")
            errors = True

        # redirect back if any error occured
        if errors:
            return render("register.html", username=username)
        
        # else, add user
        try:
            insert_user(username, generate_password_hash(password))
            flash("Registration succeeded")
            return redirect(url_for("login"))
        except Exception as e:
            flash("Error: {e}")
            return redirect(url_for("register"))

    return render("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login Page """

    session.clear()

    if request.method == "POST":
        # request form entries
        username = request.form.get("username")
        password = request.form.get("password")

        errors = False

        # required fields not empty
        if not username:
            flash("Please enter a Username")
            errors = True
        if not password:
            flash("Please enter Password")
            errors = True

        # request user from database
        user = get_users(username)
        for row in user:
            print(row["username"])

        if len(user) != 1:
            flash("User doesn't exist")
            errors = True
        elif not check_password_hash(user[0]["hash"], password):
            flash("Invalid password!")
            errors = True
        
        # redirect back if any error occured
        if errors:
            return render("login.html", username=username)
        
        # if everything went right, store users id in session
        session["user"] = user[0]["id"]
        flash(f"Successfully logged in, welcome {username}")

        return redirect(url_for("overview"))

    return render("login.html")


@app.route("/contact")
def contact():
    """ Contact page """

    # JS functionality only

    return render("contact.html")


@app.route("/impressum")
def impressum():
    """ The Impressum """

    return render("impressum.html")


@app.route("/logout")
def logout():
    """ Logout (no site itself) """

    # forget user
    session.clear()
    flash("Successfully logged out.")

    #redirect to home
    return redirect(url_for("index"))


# user sites, where login is needed from here
@app.route("/overview", methods=["GET", "POST"])
@login_required
def overview():
    """ Overview of all Tasks and quick new Task """

    if request.method == "POST":

        # task is done - check
        if "checktask" in request.form:
            # request task id
            checktask = request.form.get("checktask")
            # check
            check_task(checktask)

        # task no longer needed - delete (irreversible!)
        elif "delete" in request.form:
            # request task id
            delete = request.form.get("delete")
            # delete
            delete_task(delete)

        redirect(url_for("overview"))

    # get taskz from database
    taskz = get_taskz(session["user"])

    return render("overview.html", taskz=taskz)


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    """ New Task """

    if request.method == "POST":

        # get user inputs
        title = request.form.get("title")
        text = request.form.get("text")
        due_date = request.form.get("date")
        
        # check date format
        date_check = True
        if due_date:
            try:
                date = datetime.strptime(due_date, "%Y-%m-%d")
            except:
                date_check = False
        else:
            # no date entered? date = min
            date = datetime.min

        # everything okay? add task to database
        if title and text and date_check:
            insert_task(session["user"], title, text, date)
            flash("Task added successfully.")
        if not title:
            flash("No title entered.")
        if not text:
            flash("no text entered.")
        if not date_check:
            flash("date entered, but wrong format used ('YYYY-MM-DD')")
        
        redirect(url_for("new"))

        # optional:
        # TODO check if date not in past
        # TODO title max length?

    return render("new.html")


@app.route("/cal", methods=["GET", "POST"])
@login_required
def cal():
    """ Calendar view """

    # actual date
    this_year = datetime.now().year
    this_month = datetime.now().month

    # get date from url
    year = request.args.get("year", default = this_year, type = int)
    month = request.args.get("month", default = this_month, type = int)

    # init calendar
    cal = calendar.HTMLCalendar().formatmonth(year, month)

    # calculations for calendar navigation
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    #get taskz
    taskz = get_taskz(session["user"])

    return render("calendar.html", taskz=taskz, calendar=cal, year=year, month=month, 
                  prev_year=prev_year, prev_month = prev_month, 
                  next_year=next_year, next_month=next_month, 
                  this_year=this_year, this_month=this_month)


@app.route("/day")
@login_required
def day():
    """ Day view """

    # actual date
    this_year = datetime.now().year
    this_month = datetime.now().month
    this_day = datetime.now().day

    year = request.args.get("year", default = this_year, type = int)
    month = request.args.get("month", default = this_month, type = int)
    day = request.args.get("day", default = this_day, type = int)

    day_date = datetime.combine(date(year, month, day), time.min)

    #get taskz
    taskz = get_taskz(session["user"])

    #TODO Tage vor und zurück schalten
    #TODO Checktask integrieren

    return render("day.html", taskz=taskz, day_date=day_date)


#start app
if __name__ == "__main__":
    app.run()