from flask_app import app
import os
import urllib.request
from flask import render_template, request, redirect, url_for, flash, session, Flask
from werkzeug.utils import secure_filename
from flask_app.models.user import User
from flask_app.models.shop import Shop
from flask_app.models.product import Product
from flask_app.models.image import Image
from flask_app.controllers.products import handle_img

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_pics(shop_id):
    pics = []
    for i in range(1,11):
        print(request.files)
        temp = request.files["pic"+str(i)]
        hold = "pic"+str(i)
        print("temp is : ")
        print(temp)
        if temp.filename != "":
            temp_pic = handle_img(hold)
            data={
                "is_active": False,
                "img": temp_pic,
                "shop_id": shop_id
            }
            print("pic data is:")
            print(data)
            pics.append(data)
    print("pics is :")
    print(pics)
    if len(pics) == 0:
        return
    pics[0]["is_active"] = True
    print(pics)
    for pic in pics:
        res=Image.create(pic)
        print(res)
    return pics

@app.route('/')
def default():
    shops = Shop.get_all_shops()
    return render_template('welcome.html', shops = shops)

@app.route('/shop_setup')
def shop_setup():
    user = User.get_user(session['user_id'])
    return render_template('shop_setup.html', user = user)

@app.route('/create_shop', methods=['POST'])
def create_shop():
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    # print(f"dashboard session userid is: {session['user_id']}")
    print("create shop request from is:")
    print(request.files)
    if not Shop.validate_shop(request.form):
        flash("All fields are required.","add")
        return redirect('/shop_setup')
    if 'banner' not in request.files:
        flash("No file part")
        return redirect('/shop_setup')
    file = request.files['banner']
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect('/shop_setup')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        print("upload_image filename: " + filename)
    data ={
        "name": request.form['name'],
        "banner": filename,
        "tag_line": request.form['tag'],
        "user_id": session['user_id'],
    }
    print(f"shop created is: {data}")
    res = Shop.create(data)
    print(f"res is {res}")
    shop_id = res
    pictures = get_pics(shop_id)
    print(pictures)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_shop(id):
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')    
    shop = Shop.get_shop(id) 
    user = User.get_user(session['user_id'])
    return render_template('shop_edit.html', shop = shop, user = user)

@app.route('/update_shop', methods=['POST'])
def update_shop():
    print("update shop request from is:")
    print(request.form)
    if not Shop.validate_shop(request.form):
        flash("All fields are required.","edit")
        id=request.form['id']
        return redirect(url_for('edit_shop', id = id))
    data ={
        "id": request.form['id'],
        "name": request.form['name'],
        "banner": request.form['banner'],
        "tag_line": request.form['tag'],
        "user_id": session['user_id'],
    }
    print(f"shop updated is: {data}")
    res = Shop.update(data)    
    print(f"res is {res}")
    pictures = get_pics(request.form['id'])
    print(pictures)
    
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


@app.route("/shop/<int:id>")
def show_shop(id):
    shop = Shop.get_shop(id)
    products = Product.get_all(id)
    pictures = Image.get_all_for_shop(id)
    return render_template('shop.html', shop = shop, products = products, pictures = pictures)

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
