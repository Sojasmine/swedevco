import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_jobs")
def get_jobs():
    jobs = list(mongo.db.jobs.find())
    return render_template("jobs.html", jobs=jobs)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Sorry...username already taken!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower()
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Your registration is complete!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Check if username already exist in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(
             existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username").capitalize()))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Wrong Username and/or Password")
                return redirect(url_for("signin"))

        else:
            # username doesn't exist
            flash("Wrong Username and/or Password")
            return redirect(url_for("signin"))

    return render_template("signin.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        # jobs posted by the user appear in user's profile
        jobs = list(mongo.db.jobs.find().sort("_id, -1"))
        return render_template("profile.html", username=username, jobs=jobs)

    return redirect(url_for("signin"))


@app.route("/signout")
def signout():
    # remove user from session coikes
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("signin"))


@app.route("/post_jobs", methods=["GET", "POST"])
def post_jobs():
    if request.method == "POST":
        jobs = {
            "category_name": request.form.get("category_name"),
            "job_title": request.form.get("job_title"),
            "salary": request.form.get("salary"),
            "location": request.form.get("location"),
            "company": request.form.get("company"),
            "job_description": request.form.get("job_description"),
            "experience": request.form.get("experience"),
            "qualification": request.form.get("qualification"),
            "about_the_company": request.form.get("about_the_company"),
            "application": request.form.get("application"),
            "submit_date": request.form.get("submit_date"),
            "posted_by": session["user"]
        }
        mongo.db.jobs.insert_one(jobs)
        flash("Your posts is now published!")
        return redirect(url_for("get_jobs"))
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("post_jobs.html", categories=categories)


@app.route("/edit_jobs/<jobs_id>", methods=["GET", "POST"])
def edit_jobs(jobs_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "job_title": request.form.get("job_title"),
            "salary": request.form.get("salary"),
            "location": request.form.get("location"),
            "company": request.form.get("company"),
            "job_description": request.form.get("job_description"),
            "experience": request.form.get("experience"),
            "qualification": request.form.get("qualification"),
            "about_the_company": request.form.get("about_the_company"),
            "application": request.form.get("application"),
            "submit_date": request.form.get("submit_date"),
            "posted_by": session["user"]
        }

        mongo.db.jobs.update({"_id": ObjectId(jobs_id)}, submit)
        flash("Posts Successfully Updated")

    jobs = mongo.db.jobs.find_one({"_id": ObjectId(jobs_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_jobs.html", jobs=jobs, categories=categories)


@app.route("/delete_jobs/<jobs_id>")
def delete_jobs(jobs_id):
    mongo.db.jobs.remove({"_id": ObjectId(jobs_id)})
    flash("Post successfully deleted")
    return redirect(url_for("get_jobs"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Successfully Updated!")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted!")
    return redirect(url_for("get_categories"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
