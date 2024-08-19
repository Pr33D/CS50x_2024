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


def insert_user(username, password):
    """ insert new user to database """

    try:
        con = sql.connect(DB)
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, password))
            con.commit()
        finally:
            con.close()
    except:
        return


def get_users(username):
    """ retrieve all users from database by name """

    try:
        con = sql.connect(DB)
        try:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            users = cur.fetchall()
        finally:
            con.close()
    except:
        return
    
    return users


def get_taskz(user_id):
    """ retrieve all taskz from database by user_id """

    try:
        con = sql.connect(DB, detect_types=sql.PARSE_DECLTYPES)
        try:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM taskz WHERE user = ?", (user_id,))
            taskz = cur.fetchall()
        finally:
            con.close()
    except:
        return
    
    return taskz


def insert_task(user_id, title, text, date):
    """ insert new task to database """

    try:
        con = sql.connect(DB)
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO taskz (user, title, text, date) VALUES (?, ?, ?, ?)", (user_id, title, text, date))
            con.commit()
        finally:
            con.close()
    except:
        return


def check_task(id):
    """ check or uncheck task """

    try:
        con = sql.connect(DB)
        try:
            cur = con.cursor()
            cur.execute("SELECT checked FROM taskz WHERE id = ?", (id,))
            select = cur.fetchone()
            if select[0] == 0:
                cur.execute("UPDATE taskz SET checked = 1 WHERE id = ?", (id,))
            elif select[0] == 1:
                cur.execute("UPDATE taskz SET checked = 0 WHERE id = ?", (id,))
            con.commit()
        finally:
            con.close()
    except:
        return


def delete_task(id):
    """ delete task from database """

    try:
        con = sql.connect(DB)
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM taskz WHERE id = ?", (id,))
            con.commit()
        finally:
            con.close()
    except:
        return