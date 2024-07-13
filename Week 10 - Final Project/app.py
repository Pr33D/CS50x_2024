from flask import Flask, redirect, render_template as render, request, session, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from functions import login_required, insert_user, get_users, get_taskz

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
            return redirect("/login")
        except Exception as e:
            flash("Error: {e}")
            return redirect("/register")

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
            flash("Invalid username")
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

        return redirect("/overview")

    return render("login.html")


@app.route("/contact")
def contact():
    """ Contact page """

    # JS functionality only

    return render("contact.html")


@app.route("/impressum")
def impressum():
    """ The Apps home page """

    return render("impressum.html")


@app.route("/logout")
def logout():
    """ Logout (no site itself) """

    # forget user
    session.clear()
    flash("Successfully logged out.")

    #redirect to home
    return redirect("/")


# user sites, where login is needed from here
@app.route("/overview")
@login_required
def overview():
    """ Overview of all Tasks and quick new Task """

    taskz = get_taskz(session["user"])

    return render("overview.html", taskz=taskz)


@app.route("/new")
@login_required
def new():
    """ New Task """

    #TODO

    return render("new.html")


@app.route("/calendar")
@login_required
def calendar():
    """ Calendar view """

    #TODO

    return render("calendar.html")


@app.route("/day")
@login_required
def day():
    """ Day view """

    #TODO

    return render("day.html")


#start app
if __name__ == "__main__":
    app.run()