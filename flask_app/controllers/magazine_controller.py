from flask_app import app, bcrypt
from flask import render_template, redirect, session, request
from flask_app.models.user_model import User
from flask_app.models.magazine_model import Magazine
from flask import flash

#CREATE A NEW Magazine
@app.route("/magazine/new") #render form
def new_magazine():
    #accessed only by login
    if not "user_id" in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("new_magazine.html", user = User.get_by_id(data))

@app.route('/magazine/create', methods = ['POST']) #action route
def create_magazine():
    if not "user_id" in session:
        return redirect('/')
    data = {
        **request.form,
        "user_id" : session['user_id']
    }
    if not Magazine.validator(request.form):
        return redirect('/magazine/new')
    Magazine.create(data)
    return redirect('/dashboard')

#READ ONE MAGAZINE
@app.route("/magazine/<int:id>")
def display_one_magazine(id):
    data = { 
        "id" : id
    }
    magazine = Magazine.get_one_with_users(data)
    return render_template("show_magazine.html", magazine = magazine)


#DELETE A Magazine
@app.route('/delete/magazine/<int:id>') #destroy that specific message.id
def delete_message(id):
    data = {
        "id" : id
    }
    Magazine.delete(data)
    return redirect('/dashboard')

