from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask_app.models import user
from flask_app.models import product
from flask_app.models import shop

class Image:
    db_name = "solo_schema"
    def __init__(self , data):
        self.id = data['id']
        self.is_active = data['is_active']
        self.img = data['img']
        self.shop_id = data['shop_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_image(cls, id):
        data = {'id':id}
        query = "SELECT * FROM images WHERE id = %(id)s;"
        print(query)
        res = connectToMySQL(cls.db_name).query_db(query, data)
        print("res is :")
        print(res)
        if len(res) < 1:
            image = None
        else:
            image = cls(res[0])
        return image

    @classmethod
    def get_all_for_shop(cls, shop_id):
        data = {'shop_id': shop_id}
        query = "SELECT * FROM images WHERE shop_id= %(shop_id)s"
        print(query)
        res = connectToMySQL(cls.db_name).query_db(query, data)
        print("res is :")
        print(res)
        images = []
        for img in res:
            images.append(cls(img))
        return images

    @classmethod
    def create(cls, data):
        query = "INSERT INTO images (is_active, img, shop_id) VALUES (%(is_active)s, %(img)s, %(shop_id)s);"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(f"send msg create result is {result}")
        return result

    @classmethod
    def update(cls, data):
        query = "UPDATE images SET is_active=%(is_active)s, img=%(img)s, shop_id=%(shop_id)s, updated_at=NOW() WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(f"send msg create result is {result}")
        return result

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM images WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    # @staticmethod
    # def validate_shop(shop):
    #     is_valid = True
    #     if len(shop["name"]) < 2:
    #         flash("Shop must have a name of at least 2 characters", "shop_err")
    #         is_valid=False
    #     # if shop["banner"] == '':
    #     #     flash("You must have a banner", "shop_err")
    #     #     is_valid=False           
    #     # if len(shop["user_id"]) < 1:
    #     #     flash("Something went seriously wrong. The user associated with this shop is missing", "shop_err")
    #     #     is_valid=False
    #     return is_valid

        