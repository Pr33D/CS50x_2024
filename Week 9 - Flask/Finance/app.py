import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    stocks = db.execute("SELECT * FROM user_stocks WHERE user = ?", session["user_id"])

    # init value of all stocks owned
    stock_value = 0

    for stock in stocks:
        stock["price_act"] = lookup(stock["stock"])["price"]
        stock["total_avg"] = stock["price_avg"] * stock["count"]
        stock["total_act"] = stock["price_act"] * stock["count"]
        stock["diff"] = stock["price_act"] - stock["price_avg"]
        stock["total_diff"] = stock["total_act"] - stock["total_avg"]
        stock_value += stock["price_act"] * stock["count"]

    # combine cash and stock value
    total = user_cash + stock_value

    return render_template("index.html", stocks=stocks, cash=usd(user_cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # pick users cash for get (show) and post (maths)
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    if request.method == "POST":
        # get symbol
        symbol = request.form.get("symbol")
        if not symbol or lookup(symbol) == None:
            return apology("No valid symbol or stock not found")

        # get shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 1:
                return apology("Please enter a positive integer")
        except:
            return apology("This is not a valid number")

        price = lookup(symbol)["price"]
        total_costs = price * shares

        if total_costs > user_cash:
            return apology("Not enough money")

        # insert/update owned stocks
        select = db.execute("SELECT * FROM user_stocks WHERE user = ? AND stock = ?",
                            session["user_id"], symbol)
        # entry is there
        if select:
            # calc avg price of existing and new stocks
            price_avg = ((float(select[0]["price_avg"]) * select[0]["count"]) +
                         (total_costs)) / (select[0]["count"] + shares)
            # update user_stocks
            db.execute(""" UPDATE user_stocks SET count = count + ?,
                       price_avg = ? WHERE user = ? AND stock = ? """,
                       shares, price_avg, session["user_id"], symbol)
        # entry doesnt exist
        else:
            # insert new column to user_stocks
            db.execute("INSERT INTO user_stocks(user, stock, count, price_avg) VALUES (?, ?, ?, ?)",
                       session["user_id"], symbol, shares, price)

        # insert into transactions
        db.execute(""" INSERT INTO transactions(user, stock, price, count, action)
                   VALUES (?, ?, ?, ?, ?) """,
                   session["user_id"], symbol, price, shares, "buy")

        # user cash balance
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                   total_costs, session["user_id"])

        return redirect("/")

    return render_template("buy.html", cash=usd(user_cash))


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    sort = request.args.get("sort")

    if sort == "price":
        transactions = db.execute(
            "SELECT * FROM transactions WHERE user = ? ORDER BY price", session["user_id"])
    elif sort == "count":
        transactions = db.execute(
            "SELECT * FROM transactions WHERE user = ? ORDER BY count", session["user_id"])
    elif sort == "symbol":
        transactions = db.execute(
            "SELECT * FROM transactions WHERE user = ? ORDER BY stock", session["user_id"])
    else:
        transactions = db.execute(
            "SELECT * FROM transactions WHERE user = ? ORDER BY time", session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        # handle error exceptions
        if stock == None:
            return apology("Something went wrong")

        return render_template("quote.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure submission
        if not name or not password or not confirmation:
            return apology("Please enter fill in all fields")
        elif password != confirmation:
            return apology("Passwords didn't match")

        # inputs are valid
        try:
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)",
                       name, generate_password_hash(password))
        except ValueError:
            return apology("Name already taken")
        except:
            return apology("Something went wrong")

        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    stocks = db.execute("SELECT * FROM user_stocks WHERE user = ?", session["user_id"])

    if request.method == "POST":
        # get symbol
        symbol = request.form.get("symbol")
        # request db
        select = db.execute(
            "SELECT * FROM user_stocks WHERE user = ? AND stock = ?", session["user_id"], symbol)

        # check user owns the selected stock
        if not select:
            return apology("Not a stock you own!")

        # get shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 1:
                return apology("Please enter a positive integer")
        except:
            return apology("This is not a valid number")

        price = lookup(symbol)["price"]
        total_income = price * shares

        # compare entry and owned stocks of this type
        # abort if user wants so sell more than owned
        if shares > select[0]["count"]:
            return apology("You don't have enough shares")
        # delete stock, if it goes to zero
        elif shares == select[0]["count"]:
            db.execute(" DELETE FROM user_stocks WHERE user = ? AND stock = ? ",
                       session["user_id"], symbol)
        # else, update
        else:
            # calc new avg price
            price_avg = ((float(select[0]["price_avg"]) * select[0]["count"]) -
                         (total_income)) / (select[0]["count"] - shares)

            # insert/update owned stocks
            db.execute(""" UPDATE user_stocks SET count = count - ?,
                        price_avg = ? WHERE user = ? AND stock = ? """,
                       shares, price_avg, session["user_id"], symbol)

        # insert into transactions
        db.execute(""" INSERT INTO transactions(user, stock, price, count, action)
                   VALUES (?, ?, ?, ?, ?) """,
                   session["user_id"], symbol, price, shares, "sell")

        # user cash balance
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   total_income, session["user_id"])

        return redirect("/")

    return render_template("sell.html", cash=usd(user_cash), stocks=stocks)
