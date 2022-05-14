from flask_app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_app.models.shop import Shop
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/admin')
def admin():
    return render_template('index.html')

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_user():
    print("create reuest from is:")
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    data ={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    print(f"data for create is:{data}")
    res = User.create(data)
    print(f"res is {res}")
    session["user_id"] = res
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    print("login request from is:")
    print(request.form)
    user = User.get_user_email(request.form)
    if not user:
        flash("Invalid Email or Password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email or Password","login")
        return redirect('/')
    session['user_id'] = user.id    
    return redirect('/dashboard')


@app.route('/dashboard')
def success():
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    # print(f"dashboard session userid is: {session['user_id']}")
    user = User.get_user(session['user_id'])
    shop = Shop.get_shop(session['user_id'])
    if shop != None:
        products = Product.get_all(shop.id)
    print('success result is:')
    print(shop)
    # print(messages[0])
    if shop == None:
        return render_template('shop_setup.html', user = user)
    elif products == None:
        return render_template('dashboard.html', user = user, shop = shop)
    else:
        return render_template('dashboard.html', user = user, shop = shop, products = products)

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

@app.route("/delete_user/<int:id>")
def clean_user(id):
    data = {'id':id}
    User.delete(data)
    return redirect('/')
