from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask_app.models import user
from flask_app.models import product

class Shop:
    db_name = "solo_schema"
    def __init__(self , data):
        self.id = data['id']
        self.name = data['name']
        self.banner = data['banner']
        self.user = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_shop(cls, data):
        data = {'id':data}
        query = "SELECT * FROM shops LEFT JOIN users ON shops.user_id = users.id WHERE users.id = %(id)s;"
        print(query)
        res = connectToMySQL(cls.db_name).query_db(query, data)
        print("res is :")
        print(res)
        if len(res) < 1:
            shop = None
        else:
            shop = cls(res[0])
        return shop

    @classmethod
    def create(cls, data):
        query = "INSERT INTO shops (name, banner, user_id) VALUES (%(name)s, %(banner)s, %(user_id)s);"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(f"send msg create result is {result}")
        return result

    @classmethod
    def update(cls, data):
        query = "UPDATE shops SET name=%(name)s, banner=%(banner)s, user_id=%(user)s, updated_at=NOW() WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(f"send msg create result is {result}")
        return result

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM shops WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_shop(shop):
        is_valid = True
        if len(shop["name"]) < 2:
            flash("Shop must have a name of at least 2 characters", "shop_err")
            is_valid=False
        # if shop["banner"] == '':
        #     flash("You must have a banner", "shop_err")
        #     is_valid=False           
        # if len(shop["user_id"]) < 1:
        #     flash("Something went seriously wrong. The user associated with this shop is missing", "shop_err")
        #     is_valid=False
        return is_valid

        