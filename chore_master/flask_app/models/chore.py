from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Chore:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.user_id = data['user_id']
    
    @classmethod
    def all_chores(cls):
        query = "SELECT * FROM chores;"
        result = connectToMySQL("chore_schema").query_db(query)
        all_chores = []
        for row in result:
            all_chores.append(cls(row))
        return all_chores
    
    @classmethod
    def add_chore(cls, data):
        query = "INSERT INTO chores (title,description,location,user_id) VALUES (%(title)s,%(description)s,%(location)s,%(user_id)s);"
        result = connectToMySQL("chore_schema").query_db(query,data)
        return result
    
    @classmethod
    def user_post_chore_id(cls,data):
        query = "SELECT * FROM chores JOIN users ON users.id = chores.user_id WHERE chores.id = %(id)s"
        result = connectToMySQL("chore_schema").query_db(query,data) 
        users = []
        for row in result:
            one_user = cls(row)
            user_data = {
                "id" : row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_user.user = user.User(user_data)
            users.append(one_user)
        return users
    
    @classmethod
    def user(cls):
        query = "SELECT * FROM chores JOIN users ON users.id = chores.user_id"
        result = connectToMySQL('chore_schema').query_db(query) 
        users = []
        for row in result:
            one_user = cls(row)
            user_data = {
                "id" : row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_user.user = user.User(user_data)
            users.append(one_user)
        return users
    
    @classmethod
    def view_chore(cls, data):
        query = "SELECT * FROM chores WHERE id = %(id)s"
        result = connectToMySQL('chore_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update_chore(cls, data):
        query = "UPDATE chores SET title = %(title)s,description = %(description)s,location = %(location)s,updated_at = NOW() WHERE id = %(id)s"
        result = connectToMySQL("chore_schema").query_db(query,data)
        return result

    @staticmethod
    def validate_chore(chore):
        is_valid = True
        if len(chore['title']) < 3:
            flash("Title must be more than 2 charachters.")
            is_valid = False
        if len(chore['description']) < 1:
            flash("Description field cannot be empty. Please enter the description of the Chore.")
            is_valid = False
        if len(chore['location']) < 1:
            flash("Location field cannot be empty. Please enter the location of the Chore.")
            is_valid= False
        return is_valid
    
    @classmethod
    def delete_chore(cls,data):
        query = "DELETE FROM chores WHERE id = %(id)s"
        result = connectToMySQL("chore_schema").query_db(query,data)
        return result