from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import shop
from flask_app.models import product

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # Basic email vaildation regex
# PASSWORD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,20}$") 

class User:
    db_name="solo_schema"
    def __init__(self , data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_user(cls, data):
        data = {'id':data}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        res = connectToMySQL(cls.db_name).query_db(query, data)
        if len(res) < 1:
            return False
        user = cls(res[0])
        return user

    # @classmethod
    # def get_user(cls, data):
    #     data = {'id':data}
    #     query = "SELECT users.*, cars.* FROM users JOIN sold ON users.id = sold.user_id JOIN cars ON sold.car_id = cars.id WHERE users.id = %(id)s;"
    #     res = connectToMySQL(cls.db_name).query_db(query, data)
    #     if len(res) < 1:
    #         return False
    #     user = cls(res[0])
    #     purchases = []
    #     for row in res:
    #         print(row)
    #         car_info= {
    #             "id":row["cars.id"],
    #             "price":row["price"],
    #             "model":row["model"],
    #             "make":row["make"],
    #             "year_made":row["year_made"],
    #             "description":row["description"],
    #             "seller_id":row["seller_id"],
    #             "created_at":row["cars.created_at"],
    #             "updated_at":row["cars.updated_at"]
    #             }
    #         row = car.Car(car_info)
    #         purchases.append(row)
    #     user.purchases = purchases
    #     for p in user.purchases:
    #         print(f"p is {p}")
    #     return user

    @classmethod
    def get_other_user(cls, data):
        data = {'id':data}
        query = "SELECT * FROM users WHERE id != %(id)s;"
        res = connectToMySQL(cls.db_name).query_db(query, data)
        users = []
        for user in res:
            users.append(cls(user))
        return users

    @classmethod
    def get_user_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        res = connectToMySQL(cls.db_name).query_db(query, data)
        if len(res) < 1:
            return False
        user = cls(res[0])
        return user
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        print(f"Create data is {data}")
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(f"User create result is {result}")
        return result

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email=%(email)s"
        res = connectToMySQL('solo_schema').query_db(query,user)
        if len(res) >= 1:
            flash("That email is taken!", "register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 2:
            flash("Password must be at least 2 characters","register")
            is_valid= False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        # if not PASSWORD_REGEX.match(user['password']):
        #     flash("Invaid password! Passwords must contain at least 1 uppercase charater, 1 number, and 1 special charater","register")
        #     is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid