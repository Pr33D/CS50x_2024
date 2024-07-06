import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))

        # Check entries and insert into db if valid
        if not name or not month or month not in range(1,13) or not day or day not in range(1,32):
            return redirect("/")

        # TODO: Add the user's entry into the database
        db = sqlite3.connect("birthdays.db")
        cur = db.cursor()
        cur.execute("INSERT INTO birthdays(name, month, day) VALUES(?, ?, ?)",(name, month, day))
        db.commit()
        db.close()
        return redirect("/")

    # TODO: Display the entries in the database on index.html
    db = sqlite3.connect("birthdays.db")
    # db entries are by default returned as tuple, Row = key/value pair
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("SELECT * FROM birthdays")
    list = cur.fetchall()
    db.close()
    return render_template("index.html", list=list)
