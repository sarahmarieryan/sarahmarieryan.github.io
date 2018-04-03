from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

#pset 7 distribution code used to start this file and login, register,helpers

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
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
db = SQL("sqlite:///log.db")


@app.route("/")
@login_required
def home():
    """Show team stats for the last week for the team workout and throws"""

    #Get the number of unique players who have done wo1/wo2/wo3 at least once in the last 7 days
    w1week = len(db.execute("""SELECT COUNT(w1) FROM exercise
            WHERE user_id = :user_id AND w1 >= 1 and date >= date('now','-7 days') GROUP BY name""", user_id=session["user_id"]))

    w2week = len(db.execute("""SELECT COUNT(w2) FROM exercise
            WHERE user_id = :user_id AND w2 >= 1 and date >= date('now','-7 days') GROUP BY name""", user_id=session["user_id"]))

    w3week = len(db.execute("""SELECT COUNT(w3) FROM exercise
            WHERE user_id = :user_id AND w3 >= 1 and date >= date('now','-7 days') GROUP BY name""", user_id=session["user_id"]))

    #Get the number of unique players who have thrown at least once in the last day
    throwday = len(db.execute("""SELECT COUNT(throw) FROM exercise
            WHERE user_id = :user_id AND throw >= 1 and date >= date() GROUP BY name""", user_id=session["user_id"]))


    #Get the number of unique players
    playercount = len(db.execute("""SELECT name FROM exercise
            WHERE user_id = :user_id GROUP BY name""", user_id=session["user_id"]))

    #Get a players total exercise for the last week
    perfects = db.execute("""SELECT name, SUM(w1) AS w1, SUM(w2) AS w2, SUM(w3) AS w3, SUM(throw) AS throw FROM exercise
            WHERE user_id = :user_id and date >= date('now','-7 days') GROUP BY name""", user_id=session["user_id"])

    #nonactive players in each category for the last week
    notw1 = playercount - w1week
    notw2 = playercount - w2week
    notw3 = playercount - w3week
    notthrow = playercount - throwday




    # Render portfolio
    return render_template("home.html", w1week=w1week, notw1=notw1, w2week=w2week, notw2=notw2, w3week=w3week, notw3=notw3, throwday=throwday, notthrow=notthrow, perfects=perfects)

@app.route("/index")
@login_required
def index():
    """Display team information"""
    #all time player exercise sums
    stats = db.execute("""SELECT name, SUM(w1) AS w1, SUM(w2) AS w2, SUM(w3) AS w3, SUM(throw) AS throw, SUM(play) AS play, SUM(cardio) AS cardio, SUM(roll) AS roll, SUM(pushups) AS pushups, SUM(abs) AS abs, SUM(arms) AS arms, SUM(squats) AS squats, SUM(resistanceleg) AS resistanceleg, SUM(sldl) AS sldl, SUM(pullup) AS pullup, SUM(jump) AS jump FROM exercise
            WHERE user_id = :user_id GROUP BY name""", user_id=session["user_id"])
    #all time team exercise totals for charts
    totals = db.execute("""SELECT name, SUM(w1) AS w1, SUM(w2) AS w2, SUM(w3) AS w3, SUM(throw) AS throw, SUM(play) AS play, SUM(cardio) AS cardio, SUM(roll) AS roll, SUM(pushups) AS pushups, SUM(abs) AS abs, SUM(arms) AS arms, SUM(squats) AS squats, SUM(resistanceleg) AS resistanceleg, SUM(sldl) AS sldl, SUM(pullup) AS pullup, SUM(jump) AS jump FROM exercise
            WHERE user_id = :user_id""", user_id=session["user_id"])

    return render_template("index.html", stats=stats, totals=totals)

@app.route("/player", methods=["GET", "POST"])
@login_required
def player():
    """prompt user for player, then give player specific information and badges"""
    # POST
    if request.method == "POST":
        #User identified player
        person = request.form.get("person")

        #person's week stats
        weekstats = db.execute("""SELECT name, SUM(w1) AS w1, SUM(w2) AS w2, SUM(w3) AS w3, SUM(throw) AS throw, SUM(play) AS play, SUM(cardio) AS cardio, SUM(roll) AS roll, SUM(pushups) AS pushups, SUM(abs) AS abs, SUM(arms) AS arms, SUM(squats) AS squats, SUM(resistanceleg) AS resistanceleg, SUM(sldl) AS sldl, SUM(pullup) AS pullup, SUM(jump) AS jump FROM exercise
            WHERE user_id = :user_id and name = :name and date >= date('now','-7 days') GROUP BY name""", user_id=session["user_id"], name=person)

        #person's all time
        stats = db.execute("""SELECT name, SUM(w1) AS w1, SUM(w2) AS w2, SUM(w3) AS w3, SUM(throw) AS throw, SUM(play) AS play, SUM(cardio) AS cardio, SUM(roll) AS roll, SUM(pushups) AS pushups, SUM(abs) AS abs, SUM(arms) AS arms, SUM(squats) AS squats, SUM(resistanceleg) AS resistanceleg, SUM(sldl) AS sldl, SUM(pullup) AS pullup, SUM(jump) AS jump FROM exercise
            WHERE user_id = :user_id and name = :name GROUP BY name""", user_id=session["user_id"], name=person)


        # Display
        return render_template("playerindex.html", stats=stats, weekstats=weekstats)

    # GET
    else:
        #array of players for dropdown menu
        players = db.execute("""SELECT name FROM exercise
            WHERE user_id = :user_id GROUP BY name""", user_id=session["user_id"])

        return render_template("player.html", players=players)

@app.route("/addplayer", methods=["GET", "POST"])
@login_required
def addplayer():
    """add new player"""
    # POST
    if request.method == "POST":

        name = request.form.get("name")

        # add player to records
        db.execute("""INSERT INTO exercise (user_id, name)
            VALUES(:user_id, :name)""",
                   user_id=session["user_id"], name=name)


        # Display home
        flash("Player added!")
        return redirect("/")

    # GET
    else:

        return render_template("addplayer.html")

@app.route("/logwo1", methods=["GET", "POST"])
@login_required
def logwo1():
    """add new workout"""
    # POST
    if request.method == "POST":

        name = request.form.get("person")
        w1 = 1
        cardio = 7
        roll = 3
        abs = 12
        squats = 48
        pushups = 24
        resistanceleg = 5
        arms = 3

        # add workout to records
        db.execute("""INSERT INTO exercise (user_id, name, w1,  cardio, roll, pushups, abs, arms, squats, resistanceleg)
            VALUES(:user_id, :name, :w1, :cardio, :roll, :pushups, :abs, :arms, :squats, :resistanceleg)""",
                   user_id=session["user_id"], name=name, w1=w1, cardio=cardio, roll=roll, pushups=pushups, abs=abs, arms=arms, squats=squats, resistanceleg=resistanceleg)



        # Display home
        flash("Lift added!")
        return redirect("/")

    # GET
    else:
        #array of players for dropdown menu
        players = db.execute("""SELECT name FROM exercise
            WHERE user_id = :user_id GROUP BY name""", user_id=session["user_id"])

        return render_template("logwo1.html", players=players)

@app.route("/logwo2", methods=["GET", "POST"])
@login_required
def logwo2():
    """add new workout"""
    # POST
    if request.method == "POST":

        name = request.form.get("person")
        w2 = 1
        throw =1
        cardio = 35
        roll = 5

        # add workout 2 to records
        db.execute("""INSERT INTO exercise (user_id, name, w2, throw, cardio, roll)
            VALUES(:user_id, :name, :w2, :throw, :cardio, :roll)""",
                   user_id=session["user_id"], name=name, w2=w2, throw=throw, cardio=cardio, roll=roll)



        # Display home
        flash("Workout added!")
        return redirect("/")

    # GET
    else:
        #array of players for dropdown menu
        players = db.execute("""SELECT name FROM exercise
            WHERE user_id = :user_id GROUP BY name""", user_id=session["user_id"])

        return render_template("logwo2.html", players=players)

@app.route("/logwo3", methods=["GET", "POST"])
@login_required
def logwo3():
    """add new workout"""
    # POST
    if request.method == "POST":

        name = request.form.get("person")
        w3 = 1
        cardio = 35
        roll = 5
        abs = 6
        sldl = 32


        # add workout 3 to records
        db.execute("""INSERT INTO exercise (user_id, name, w3, cardio, roll, abs, sldl)
            VALUES(:user_id, :name, :w3, :cardio, :roll, :abs, :sldl)""",
                   user_id=session["user_id"], name=name, w3=w3, cardio=cardio, roll=roll, abs=abs, sldl=sldl)




        # Display home
        flash("Workout added!")
        return redirect("/")

    # GET
    else:
        #array of players for dropdown menu
        players = db.execute("""SELECT name FROM exercise
            WHERE user_id = :user_id GROUP BY name""", user_id=session["user_id"])

        return render_template("logwo3.html", players=players)

@app.route("/logthrow", methods=["GET", "POST"])
@login_required
def logthrow():
    """add new throw"""
    # POST
    if request.method == "POST":

        name = request.form.get("person")
        throw = 1

        # add throw to records
        db.execute("""INSERT INTO exercise (user_id, name, throw)
            VALUES(:user_id, :name, :throw)""",
                   user_id=session["user_id"], name=name, throw=throw)


        # Display home
        flash("Throwing session added!")
        return redirect("/")

    # GET
    else:
        #array of players for dropdown menu
        players = db.execute("""SELECT name FROM exercise
            WHERE user_id = :user_id GROUP BY name""", user_id=session["user_id"])

        return render_template("logthrow.html", players=players)

@app.route("/logother", methods=["GET", "POST"])
@login_required
def logother():
    """add new workout"""
    # POST
    if request.method == "POST":

        name = request.form.get("person")
        play = request.form.get("play")
        cardio = request.form.get("cardio")
        roll = request.form.get("roll")
        pushups = request.form.get("pushups")
        abs = request.form.get("abs")
        arms = request.form.get("arms")
        squats = request.form.get("squats")
        resistanceleg = request.form.get("resistanceleg")
        sldl = request.form.get("sldl")
        pullup = request.form.get("pullup")
        jump = request.form.get("jump")

        # add workout to records
        db.execute("""INSERT INTO exercise (user_id, name, play, cardio, roll, pushups, abs, arms, squats, resistanceleg, sldl, pullup, jump)
            VALUES(:user_id, :name, :play, :cardio, :roll, :pushups, :abs, :arms, :squats, :resistanceleg, :sldl, :pullup, :jump)""",
                   user_id=session["user_id"], name=name, play=play, cardio=cardio, roll=roll, pushups=pushups, abs=abs, arms=arms, squats=squats, resistanceleg=resistanceleg, sldl=sldl, pullup=pullup, jump=jump)


        # Display home
        flash("Workout added!")
        return redirect("/")

    # GET
    else:
        #array of players for dropdown menu
        players = db.execute("""SELECT name FROM exercise
            WHERE user_id = :user_id GROUP BY name""", user_id=session["user_id"])

        return render_template("logother.html", players=players)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                        username=request.form.get("username"),
                        hash=generate_password_hash(request.form.get("password")))
        if not id:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("register.html")



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
