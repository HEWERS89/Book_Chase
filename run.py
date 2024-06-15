import os
from flask import (
    Flask, render_template, url_for, 
    redirect, flash, request, session, g
)
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

client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
db = client["book_chase"]
books = db["books"]
reviews = db["reviews"] 


def authenticated_user():
    if 'user' in session:
        return True
    return False

# Initialize current_user
@app.before_request
def before_request():
    g.current_user = None
    if 'user' in session:
        g.current_user = session['user']

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

@app.route("/logout")
def logout():
    session.pop('user', None)
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get('search')
        if not query or query.strip() == '':
            flash('Please enter a search query.')
            return redirect(url_for('search'))

        books = list(db.books.find({"$or": [{"title": {"$regex": query, "$options": "i"}}, {"author": {"$regex": query, "$options": "i"}}, {"isbn": {"$regex": query, "$options": "i"}}]}))
        if books:
            return render_template("search.html", books=books, show_results=True)
        else:
            flash("No books found.")
    return render_template("search.html", show_results=False)

@app.route('/books/<book_id>/review', methods=['GET', 'POST'])
def book_review(book_id):
    if not authenticated_user():
        return redirect(url_for('log_in', next=request.url))

    user_id = session['user']

    book = db.books.find_one({'_id': ObjectId(book_id)})
    if not book:
        flash('No book found')

    reviews = db.reviews.find({'book_id': ObjectId(book_id)})

    if request.method == 'POST':
        # Check if the user has already reviewed this book
        existing_review = db.reviews.find_one({'book_id': ObjectId(book_id), 'username': user_id})
        if existing_review:
            flash('You have already reviewed this book.')
        else:
            review = {
                '_id': ObjectId(),  # generate a unique ID for the review
                'book_id': ObjectId(book_id),
                'username': user_id,
                'comment': request.form.get('comment')
            }
            db.reviews.insert_one(review)
            flash('Review added successfully!')

    return render_template('book_review.html', book=book, reviews=reviews)

@app.route('/edit_review/<review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    #...
    review = db.reviews.find_one({'_id': ObjectId(review_id)})
    if not review:
        flash('Review not found', 'warning')
        return redirect(url_for('profile', username=session['user']))

    book_id = review['book_id']  
    book = db.books.find_one({'_id': ObjectId(book_id)})
    if not book:
        flash('Book not found', 'warning')
        return redirect(url_for('profile', username=session['user']))

    book_title = book['title']  

    if request.method == 'GET':
        return render_template('edit_review.html', review=review, book_title=book_title, review_id=review_id)


    if request.method == 'POST':
        comment = request.form.get('comment', '') 
        comment = request.form['comment']
        db.reviews.update_one({"_id": ObjectId(review_id)}, {"$set": {'comment': comment}})
        flash('Comment updated successfully!')
        return redirect(url_for('profile', username=session['user']))

@app.route('/delete_review/<review_id>', methods=['POST'])
def delete_review(review_id):
    if 'user' not in session:
        flash('You need to be logged in to delete a review', 'warning')
        return redirect(url_for('log_in'))

    review = db.reviews.find_one({'_id': ObjectId(review_id)})
    if not review:
        flash('Review not found', 'warning')
        return redirect(url_for('profile', username=session['user']))

    if review['username'] != session['user']:
        flash('You can only delete your own reviews', 'warning')
        return redirect(url_for('profile', username=session['user']))

    db.reviews.delete_one({"_id": ObjectId(review_id)})
    flash('Review deleted successfully!')
    return redirect(url_for('profile', username=session['user']))

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if request.method == "POST":
        # Handle POST request
        pass

    if "user" in session:
        current_user = session["user"]
        if current_user != username:
            flash("You can only view your own profile", "warning")
            return redirect(url_for("log_in"))

        user = db.users.find_one({"username": current_user})
        reviews = db.reviews.find({"username": current_user})
        count = db.reviews.count_documents({"username": current_user})

        book_reviews = []
        for review in reviews:
            book_id = review["book_id"]
            book = db.books.find_one({"_id": ObjectId(book_id)})
            if book:
                book_title = book["title"]
                comment = review["comment"]
                review_id = review["_id"]
                book_reviews.append({"book_title": book_title, "comment": comment, "review_id": review_id})

    user_books = []
    if "books" in user:
        for book_id in user["books"]:
            book = db.books.find_one({"_id": ObjectId(book_id)})
            if book:
                title = book["title"]
                author = book["author"]
                isbn = book["isbn"]
                user_books.append({"book_id": book_id, "title": title, "author": author, "isbn": isbn})

        user_books.sort(key=lambda x: x['book_id'], reverse=True)

        return render_template(
        "profile.html",
        book_reviews=book_reviews,
        user_books=user_books,
        title="My Profile",
        user=user,
        count=count,
        book_count=len(user_books))

    else:
        flash("You need to be logged in to see your profile", "warning")
        return redirect(url_for("log_in"))

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        # Check if the book already exists in the database
        existing_book = db.books.find_one({"$and": [{"title": title}, {"author": author}, {"isbn": isbn}]})

        if not existing_book:
            # Book doesn't exist, add it to the database
            book = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "added_by": session["user"]  # Add the current user to the book document
            }
            db.books.insert_one(book)
            user = db.users.find_one({"username": session["user"]})
            if "books" not in user:
                user["books"] = []
            user["books"].append(book["_id"])
            db.users.update_one({"username": session["user"]}, {"$set": user})
            flash("Book added successfully!")
            return redirect(url_for('index'))
        else:
            flash("Book already exists in the collection.")
    return render_template("add_book.html")

@app.route('/edit_book/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if request.method == 'GET':
        book = db.books.find_one({'_id': ObjectId(book_id)})
        if not book:
            flash('Book not found', 'warning')
            return redirect(url_for('profile', username=session['user']))
        return render_template('edit_book.html', book=book, book_id=book_id)

    elif request.method == 'POST':
        title = request.form.get('title', '')
        author = request.form.get('author', '')
        isbn = request.form.get('isbn', '')
        db.books.update_one({"_id": ObjectId(book_id)}, {"$set": {'title': title, 'author': author, 'isbn': isbn}})
        flash('Book updated successfully!')
        return redirect(url_for('profile', username=session['user']))

@app.route('/delete_book/<book_id>', methods=['POST'])
def delete_book(book_id):
    if 'user' not in session:
        flash('You need to be logged in to delete a book', 'warning')
        return redirect(url_for('log_in'))
    book = db.books.find_one({'_id': ObjectId(book_id)})
    if book['added_by']!= session['user']:
        flash('You can only delete your own books', 'warning')
        return redirect(url_for('profile', username=session['user']))
    db.books.delete_one({"_id": ObjectId(book_id)})
    flash('Book deleted successfully!')
    return redirect(url_for('profile', username=session['user']))

if  __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
            )


