from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Recipe:
    db = "recipes_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.under_30 = data["under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.user = {}


    @classmethod
    def create_new_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, NOW(), NOW(), %(user_id)s)"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query,)
        user_recipes = []
        for dict in results:
            user_recipes = cls(dict)
            user_data = {
                'id' : dict['users.id'],
                'first_name' : dict["first_name"],
                'last_name' : dict["last_name"],
                'email' : dict["email"],
                'password' : dict["password"],
                'created_at' : dict["user.created_at"],
                'updated_at' : dict["users.updated_at"]
            }

            user_recipes = user_model.User(user_data)
            user_recipes.append(user_recipes)



        return user_recipes


    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results



    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, updated_at = now() WHERE id = %(id)s;" 

        results = connectToMySQL(cls.db).query_db(query, data)
        return results