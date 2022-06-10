import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    stocks = []
    """Show portfolio of stocks"""
    stocks =  db.execute("SELECT * FROM stocks JOIN portfolio ON portfolio.id = stocks.portfolio_id WHERE portfolio.user_id= ?", session["user_id"])
    cash = round(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"],2)
    total = cash
    for stock in stocks:
        total += stock["per_price"] * stock["amount"]
    total = round(total,2)
    return render_template("index.html",stocks=stocks,cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock_symbol = request.form.get("stock_symbol")
        amount = request.form.get("amount")
        amount = int(amount)
        stock = lookup(stock_symbol)
        if stock != None and amount > 0:
            has_stocks = db.execute("SELECT * FROM stocks JOIN portfolio ON portfolio.id = stocks.portfolio_id WHERE portfolio.user_id= ? AND stock_symbol = ?", session["user_id"],stock["symbol"])
            portfolio_id =  db.execute("SELECT id FROM portfolio WHERE user_id= ?", session["user_id"])[0]["id"]
            db.execute("INSERT INTO transactions (datetime_text, transaction_type, stock_symbol, amount, total,portfolio_id) VALUES (datetime('now'),?, ?, ?, ?, ?)","BUY",stock["symbol"],amount,amount * stock["price"],portfolio_id)
            #if the the user already owns the stock
            if has_stocks != []:
                #update add the amount of stock the user bought to what they already have
                db.execute("UPDATE stocks SET amount = amount + ?, per_price = ? WHERE portfolio_id = ? AND stock_symbol = ?",amount, stock["price"], portfolio_id, stock["symbol"])
            #if the user doesn't have the stock add to the stock the user own, by how much they bought
            else:
                db.execute("INSERT INTO stocks (stock_symbol, name, per_price, amount, portfolio_id) VALUES (?, ?, ?, ?, ?)",stock["symbol"], stock["name"], stock["price"], amount, portfolio_id)
            #take the cash away from the user
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?;", amount * stock["price"], session["user_id"])

        return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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
    if (request.method == "POST"):
        quote = lookup(request.form.get("stock_symbol"))
        print(quote)
        return render_template("quoted.html",quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method == "POST"):
        username = request.form.get("username")
        usernames = db.execute("SELECT username FROM users")
        if ({"username":username} not in usernames):
            password = request.form.get("password")
            hash = generate_password_hash(password)
            session["user_id"] = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            portfolio_id = db.execute("INSERT INTO portfolio (user_id) VALUES (?)", session["user_id"])
            db.execute("UPDATE users SET portfolio_id = ? WHERE id = ?",portfolio_id, session["user_id"])
            return redirect("/")
        else:
            return apology(f"there's already a username: {username}")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute("SELECT * FROM stocks JOIN portfolio ON portfolio.id = stocks.portfolio_id WHERE portfolio.user_id= ?", session["user_id"])
    print(stocks)
    if request.method == "POST":
        stock_symbol = request.form.get("Symbol")
        if (stock_symbol == ""):
            return apology("Missing Symbol")
        amount = request.form.get("amount")
        stock = lookup(stock_symbol)
        amount = int(amount)
        portfolio_id =  db.execute("SELECT id FROM portfolio WHERE user_id= ?", session["user_id"])[0]["id"]
        db.execute("INSERT INTO transactions (datetime_text, transaction_type, stock_symbol, amount, total,portfolio_id) VALUES (datetime('now'),?, ?, ?, ?, ?)","SELL",stock["symbol"],amount,amount * stock["price"],portfolio_id)
        db.execute("UPDATE stocks SET amount = amount - ?, per_price = ? WHERE portfolio_id = ? AND stock_symbol = ?",amount, stock["price"], portfolio_id, stock["symbol"])
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?;", amount * stock["price"], session["user_id"])
        return redirect("/")
    return render_template("sell.html", stocks = stocks)
