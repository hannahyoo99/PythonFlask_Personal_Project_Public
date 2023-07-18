from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, bcrypt
from flask_app.models import user_model
from flask_app import DATABASE
from flask import flash


class Magazine:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        
    #CREATE NEW MESSAGE
    @classmethod
    def create(cls, data):
        query = "INSERT INTO magazines (title, description, user_id) VALUE (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data) 

    #GET ALL MAGAZINES WITH ALL USERS
    @classmethod
    def get_all_with_users(cls, data):
        query = "SELECT * FROM magazines JOIN users on user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            all_mags = []
            for row in results:
                magazine_instance = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                user_instance = user_model.User(user_data)
                magazine_instance.user = user_instance
                all_mags.append(magazine_instance)
            return all_mags
        return results

    #GET ONE MAGAZINE
    @classmethod 
    def get_one_with_users(cls, data):
        query = "SELECT * FROM magazines JOIN users ON user_id = users.id WHERE magazines.id = %(id)s;"
        results  = connectToMySQL(DATABASE).query_db(query, data)
        if results: #protects if there is an empty list 
            magazine_instance = cls(results[0])
            user_data = {
                **results[0],
                'id': results[0]['users.id'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at']
            }
            user_instance = user_model.User(user_data)
            magazine_instance.user = user_instance
            return magazine_instance
        return results

    # DELETE
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM magazines WHERE magazines.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validator(user):
        is_valid = True
        if len(user['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters", "mag")
        if len(user['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters", "mag")
        return is_valid