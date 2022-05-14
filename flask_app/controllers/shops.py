from flask_app import app
import os
import urllib.request
from flask import render_template, request, redirect, url_for, flash, session, Flask
from werkzeug.utils import secure_filename
from flask_app.models.user import User
from flask_app.models.shop import Shop

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        "user_id": session['user_id'],
    }
    print(f"shop created is: {data}")
    res = Shop.create(data)
    print(f"res is {res}")
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_shop(id):
    if 'user_id' not in session:
        flash("Please login to view content","bad_user")
        return redirect('/')
    data = {'id':id}
    shop = Shop.get_shop(data) 
    user = User.get_user(session['user_id'])
    return render_template('edit.html', shop = shop, user = user)

@app.route('/update_shop', methods=['POST'])
def update_shop():
    print("update shop request from is:")
    print(request.form)
    if not Shop.validate_shop(request.form):
        flash("All fields are required.","edit")
        id=request.form['id']
        return redirect(url_for('edit_shop', id = id))
    data ={
        "name": request.form['name'],
        "banner": request.form['banner'],
        "user_id": session['user_id'],
    }
    print(f"shop updated is: {data}")
    res = Shop.update(data)
    print(f"res is {res}")
    return redirect('/dashboard')

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
