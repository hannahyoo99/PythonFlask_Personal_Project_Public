from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, bcrypt
from flask_app import DATABASE
from flask_app.models import magazine_model
from flask import flash
import re # the regex module
# create a regular expression object that we'll use later 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    # READ ALL METHOD
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        #print results
        all_users = []
        for row_from_db in results:
            user_instance = cls(row_from_db)
            all_users.append(user_instance)
        return all_users

    #CREATE
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUE (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data) #will return id

    #READ ONE PULLED BY ID
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;" 
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) < 1: # Didn't find a matching user
            return False
        return cls(result[0])

    #READ ONE PULLED BY EMAIL
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;" 
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s" \
            "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #DELETE
    @classmethod 
    def delete (cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #READ ONE WITH List of magazines
    @classmethod 
    def get_magazines(cls, data):
        query = "SELECT * FROM users LEFT JOIN magazines ON magazines.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results: # if there is at least on thing in my list results
            user_instance = cls(results[0])
            magazine_list = []
            for row_in_db in results:
                data = {
                    **row_in_db, 
                    "id" : row_in_db['magazines.id'], #these are ambiguous fields
                    "created_at" : row_in_db['magazines.created_at'],
                    "updated_at" : row_in_db['magazines.updated_at']
                }
                magazine_instance = magazine_model.Magazine(data)
                magazine_list.append(magazine_instance)
            user_instance.list_magazines = magazine_list # this creates new attribute
            return user_instance
        return results

    #VALIDATE
    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First Name must be at least 3 characters", "regstr")
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Last Name must be at least 3 characters", "regstr")
        if len(user['email']) < 1:
            flash("Please provide email", "regstr")
            is_valid=False
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "regstr")
            is_valid = False
        else:
            data = {
                'email' : user['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                is_valid = False
                flash("Email already taken", "regstr")
        if len(user['password']) < 8:
            flash("Passwords must be at least 8 characters", "regstr")
            is_valid = False
        elif not user['password'] == user['confirm_password']:
            flash("Passwords don't match", "regstr")
            is_valid = False
        return is_valid

    @staticmethod
    def validator(user):
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First Name must be at least 3 characters", "account")
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Last Name must be at least 3 characters", "account")
        if len(user['email']) < 1:
            flash("Please provide email", "account")
            is_valid=False
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "account")
            is_valid = False
        else:
            data = {
                'email' : user['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                is_valid = False
                flash("Email already taken", "account")
        return is_valid




