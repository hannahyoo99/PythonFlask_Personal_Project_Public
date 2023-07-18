from flask_app import app, bcrypt
from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app.models.magazine_model import Magazine
import re # the regex module
# create a regular expression object that we'll use later 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#READ ALL route
@app.route('/') #display login registration
def index(): 
    return render_template("index.html") 

#DASHBOARD WITH ALL MAGAZINES
@app.route('/dashboard') 
def dashboard():
    #accessed only by login
    if not "user_id" in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("dashboard.html", user = User.get_by_id(data),\
        magazines = Magazine.get_all_with_users(data), users = User.get_all())

#CREATE A USER
@app.route('/register/user', methods = ["POST"]) #action route
def register():
    if not User.validate(request.form):
        return redirect("/")
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        **request.form,
        "password" : pw_hash
    }
    # Call the create @classmethod on User
    user_id = User.create(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/dashboard")

#LOGIN
@app.route('/login', methods=['POST']) #action route
def login():
    # see if the username provided exists in the database
    data = { 
        "email" : request.form['email'] 
    }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Credentials", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Credentials", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

#Account page
@app.route("/user/account")
def show_account():
    #accessed only by login
    if not "user_id" in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    this_user = User.get_magazines(data)
    print(this_user.first_name)
    return render_template("user_account.html", this_user = this_user)

@app.route("/update", methods=['POST'])
def update():
    data = {
        **request.form,
        "id": session['user_id']
    }
    user= User.get_by_id(data)
    if not User.validator(request.form):
        return redirect("/user/account")
    User.update(data)
    return redirect("/user/account")


@app.route("/logout")
def logout():
    #clear session
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run (debug = True)