from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask_app.models import user
from flask_app.models import shop

class Product:
    db_name = "solo_schema"
    def __init__(self , data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.img1 = data['img1']
        self.img2 = data['img2']
        self.type = data['type']
        self.shop_id = data['shop_id']
        self.price = data['price']
        self.quantity = data['quantity']
        self.purchaser_id = None
        self.order_id = None
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM products LEFT JOIN shops ON products.id = shop.id;"
    #     res = connectToMySQL(cls.db_name).query_db(query)
    #     products = []
    #     for row in res:
    #         print(row)
    #         user_info= {
    #             "id":row["users.id"],
    #             "first_name":row["first_name"],
    #             "last_name":row["last_name"],
    #             "email":row["email"],
    #             "password":row["password"],
    #             "created_at":row["users.created_at"],
    #             "updated_at":row["users.updated_at"]
    #             }
    #         row = cls(row)
    #         row.seller = user.User(user_info)
    #         row.sold = cls.get_sold(row.id)
    #         cars.append(row)
    #     return products

    def get_all(cls, data):
        data = {'id':data}
        query = "SELECT * FROM products LEFT JOIN shops ON products.shop_id = shops.id WHERE shops.id = %(id)s;"
        res = connectToMySQL(cls.db_name).query_db(query, data)
        products = []
        print(res)
        if res == False:
            return res
        else:
            for row in res:
                print(row)
                row = cls(row)
                products.append(row)
        return products

    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM products WHERE id = %(id)s;"
    #     res = connectToMySQL(cls.db_name).query_db(query, data)
    #     if len(res) < 1:
    #         return False
    #     result = cls(res[0])
    #     for row in res:
    #         user_info= {
    #             "id":row["users.id"],
    #             "first_name":row["first_name"],
    #             "last_name":row["last_name"],
    #             "email":row["email"],
    #             "password":row["password"],
    #             "created_at":row["users.created_at"],
    #             "updated_at":row["users.updated_at"]
    #         }
    #     result.seller = user.User(user_info)
    #     result.sold = cls.get_sold(result.id)
    #     return result
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        res = connectToMySQL(cls.db_name).query_db(query, data)
        if len(res) < 1:
            return False
        result = cls(res[0])
        return result

    @classmethod
    def create(cls, data):
        print("data is: ")
        print(data)
        query = "INSERT INTO products (title, description, img1, img2, type, shop_id, price, quantity, purchaser_id, order_id) VALUES (%(title)s, %(description)s, %(img1)s, %(img2)s, %(type)s, %(shop_id)s, %(price)s, %(quantity)s, %(purchaser_id)s, %(order_id)s);"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(f"send msg create result is {result}")
        return result

    @classmethod
    def update(cls, data):
        query = "UPDATE products SET title=%(title)s, description=%(description)s, img1=%(img1)s, img2=%(img2)s, type=%(type)s, shop_id=%(shop_id)s, price=%(price)s, quantity=%(quantity)s, updated_at=NOW() WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(f"send msg create result is {result}")
        return result

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM products WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_product(product):
        is_valid = True
        if len(product["title"]) < 5:
            flash("Title must be at least 5 characters long", "product_err")
            is_valid=False
        if len(product["description"]) < 1:
            flash("description field cannot be empty", "product_err")
            is_valid=False
        # if len(product["img1"]) < 1:
        #     flash("Every product must have at least 1 image", "product_err")
        #     is_valid=False
        if len(product["type"]) < 1:
            flash("You must input a type", "product_err")
            is_valid=False           
        if float(product["price"]) < 1:
            flash("Price cannot be empty", "product_err")
            is_valid=False
        if int(product["quantity"]) < 1:
            flash("Quantity cannot be empty", "product_err")
            is_valid=False
        return is_valid

        