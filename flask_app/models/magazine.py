from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Magazine:

    db_name = "magazine_schema"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.users_who_subscribe = []



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM magazines"
        results = connectToMySQL(cls.db_name).query_db(query)
        return results



    @classmethod 
    def create_magazine(cls, data):
        query = "INSERT INTO magazines (title, description,user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results


    @classmethod
    def get_magazine(cls, data):
        all_magazines = []
        query = "SELECT * FROM magazines WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        
        for result in results:
            all_magazines.append(result)
        print(all_magazines)
        return all_magazines


    @classmethod
    def get_one_magazine(cls,data):
        query = "SELECT * FROM magazines WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )


    @classmethod
    def update_magazine(cls, data):
        query = "UPDATE magazines SET title = %(title)s, description = %(description)s, WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results



    @classmethod
    def subscribe_to_magazine(cls, data):
        query = "INSERT INTO subscribes (user_id, magazine_id) VALUES (%(user_id)s, %(magazine_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results



    @classmethod
    def remove_subscribe_from_magazine(cls, data):
        query = "DELETE FROM subscribes WHERE user_id = %(user_id)s AND magazine_id = %(magazine_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results



    @classmethod
    def get_all_subscribed_magazines(cls, data):
        magazines_subscribed = []
        query = "SELECT * FROM subscribes JOIN users ON users.id = subscribes.user_id "\
        "LEFT JOIN magazines ON magazines.id = subscribes.magazine_id WHERE subscribes.user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)

        for result in results:
            magazines_subscribed.append(result)
        
        print(magazines_subscribed)
        return magazines_subscribed



    @classmethod
    def show_all_magazines_and_users(cls):
        query = "SELECT magazines.title, users.first_name, users.last_name, magazines.id, magazines.user_id, COUNT(subscribes.magazine_id) AS subscribers FROM magazines "\
        "LEFT JOIN users ON users.id = magazines.user_id "\
        "LEFT JOIN subscribes ON magazines.id = subscribes.magazine_id "\
        "GROUP by magazines.id "\
        "ORDER BY magazines.title ASC;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results



    @classmethod
    def destroy_magazine(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results



    @staticmethod
    def validate_magazine(magazine):
        is_valid = True
        if len(magazine['title']) < 2:
            is_valid = False
            flash("Title field should be at least 2 characters long","magazine")
        if len(magazine['description']) < 10:
            is_valid = False
            flash("Description field should be at least 10 characters long","magazine")
        return is_valid



    @classmethod
    def get_one_magazine_and_one_user(cls, data):
        query = "SELECT * FROM magazines LEFT JOIN users ON users.id = magazines.user_id WHERE magazines.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        return results


    @classmethod
    def get_magazines_of_user(cls,data):
        query = "SELECT magazines.id, magazines.title, magazines.user_id, COUNT(magazine_id) AS subscribers FROM magazines "\
        "LEFT JOIN subscribes on magazines.id = subscribes.magazine_id "\
        "WHERE magazines.user_id = %(id)s "\
        "GROUP BY magazines.id "\
        "ORDER BY title ASC;"

        results = connectToMySQL(cls.db_name).query_db(query,data)

        print(results)
        return(results)

    @classmethod
    def get_all_subscribers_of_one_magazine(cls,data):
        query = "SELECT magazines.title, users2.first_name, users2.last_name FROM users "\
        "LEFT JOIN magazines ON users.id = magazines.user_id "\
        "LEFT JOIN subscribes ON magazines.id = subscribes.magazine_id "\
        "JOIN users AS users2 ON users2.id = subscribes.user_id "\
        "WHERE magazines.id = %(id)s;"

        results = connectToMySQL(cls.db_name).query_db(query,data)

        print(results)
        return (results)