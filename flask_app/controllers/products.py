from flask_app import app
import os
import urllib.request
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from flask_app.models.user import User
from flask_app.models.shop import Shop
from flask_app.models.product import Product

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/photo_upload', methods=['POST'])
def photo_upload():
    print(request.files)
    # img = handle_img(request.form[])
    return redirect('/add')

def handle_img(img):
    print("hand_img img is : " + img)
    if img not in request.files:
        flash("No file part")
        return redirect('/add')
    file = request.files[img]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect('/add')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        print("upload_image filename: " + filename)
        return filename

@app.route('/create_product', methods=['POST'])
def create_product():
    shop = Shop.get_shop(session['user_id'])
    print(shop.id)
    print("create product request from is:")
    print(request.form)
    if not Product.validate_product(request.form):
        flash("All fields are required. Number of Sasquach must be at least 1.","add")
        return redirect('/add')
    img1 = handle_img("img1")
    img2 = handle_img("img2")

    data ={
        "title": request.form['title'],
        "description": request.form['description'],
        "img1": img1,
        "img2": img2,
        "type": request.form['type'],
        "shop_id": shop.id,
        "price": request.form['price'],
        "quantity": request.form['quantity'],
        "purchaser_id": None,
        "order_id": None
    }
    print(f"product created is: {data}")
    res = Product.create(data)
    print(f"res is {res}")
    return redirect('/dashboard')

@app.route('/add')
def add_product():
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    user = User.get_user(session['user_id'])
    shop = Shop.get_shop(session['user_id'])
    return render_template('add.html', user = user, shop = shop)

@app.route('/read/<int:id>')
def read_product(id):
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    data = {'id':id}
    user = User.get_user(session['user_id'])
    product = product.get_one(data) 
    return render_template('show.html', product = product, user = user)

@app.route('/edit_prod/<int:id>')
def edit_product(id):
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    data = {'id':id}
    product = Product.get_one(data) 
    user = User.get_user(session['user_id'])
    return render_template('edit.html', product = product, user = user)

@app.route('/update_product', methods=['POST'])
def update_product():
    print("update product request from is:")
    print(request.form)
    print("req files is:")
    print(request.files)
    file1 = request.files["img1"]
    file2 = request.files["img2"]
    # print("narb is: ")
    # print(narb.filename)
    # if "img1" not in request.files:
    if file1.filename == "":
        print("hit")
        img1 = request.form["img1_backup"]
    else:
        img1 = handle_img("img1")        
    if file2.filename == "":
        img2 = request.form["img2_backup"]
    else:
        img2 = handle_img("img2")        
    shop = Shop.get_shop(session['user_id'])
    if not Product.validate_product(request.form):
        flash("All fields are required. Number of Sasquach must be at least 1.","edit")
        id=request.form['id']
        return redirect(url_for('edit_product', id = id))
    data ={
        "id": request.form['id'],
        "title": request.form['title'],
        "description": request.form['description'],
        "img1": img1,
        "img2": img2,
        "type": request.form['type'],
        "shop_id": shop.id,
        "price": request.form['price'],
        "quantity": request.form['quantity'],
    }
    print(f"product updated is: {data}")
    res = Product.update(data)
    print(f"res is {res}")
    return redirect('/dashboard')

@app.route('/purchase/<int:id>')
def purchase(id):
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    data = {
        'product_id':id,
        'user_id':  session['user_id']
        }
    res = Product.sold(data)
    print(res)
    return redirect('/dashboard')

@app.route('/show_prod/<int:id>')
def show_prod(id):
    data = {'id':id}
    product = Product.get_one(data)
    return render_template('show_prod.html', product = product)

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/delete_product/<int:id>')
def result(id):
    data = {'id':id}
    Product.destroy(data)
    return redirect('/dashboard')