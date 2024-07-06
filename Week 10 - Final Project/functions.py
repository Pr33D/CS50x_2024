from functools import wraps
from flask import request, redirect, session
import sqlite3 as sql


# Database config
DB = "main.db"


def login_required(f):
    """ 
    Actual flask login required self-calling function
     
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/ 
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def insertUser(username, password):
    """ insert new user to database """

    con = sql.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, password))
    con.commit()
    con.close()


def retrieveUsers(username):
    """ retrieve users from database by name """

    con = sql.connect(DB)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", [username])
    users = cur.fetchall()
    con.close()
    return users