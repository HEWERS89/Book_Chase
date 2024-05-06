import os
from flask import (
    Flask, render_template, url_for, 
    redirect, flash, request, session)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
import pymongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# mongo = PyMongo(app)
client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
db = client["book_chase"]
print(db)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # check if username already exists in database
        existing_user = db.users.find_one(
           {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")

@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        # check if the username exists
        existing_user = db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # authorise password with username provided
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
                
    
            else:
                # invalid password 
                flash("Incorrect username and/or password")
                return redirect(url_for("log_in"))
        else:
            # username does not exist
            flash("Incorrect username and/or password used")
            return redirect(url_for("log_in"))

    return render_template("log_in.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if request.method == "POST":
        # Handle POST request (e.g., update profile)
        pass

    if 'user' in session:
        # only let a logged in user edit their own profile page
        current_user = session['user']
        flash('Hi "' + current_user + '". This is your profile '
              'page. You can view a summary of your reviews ')
        # finding user based on login session
        username = db.users.find_one({'username': current_user})
        # setting db username to the current session username
        reviews = db.reviews.find({'username': current_user})
        count = db.reviews.count_documents({'username': current_user})
        return render_template("profile.html",
                               reviews=reviews,
                               title='My Profile',
                               user=username,
                               count=count)
    else:
        # if user is not logged in
        flash('You need to be logged in to see your profile', 'warning')
        return render_template('log_in.html')
    

@app.route("/search", methods=["GET", "POST"])
def search():
    
    return render_template("search.html")






if  __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
              )


