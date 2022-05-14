from flask import Flask
from . import vault

UPLOAD_FOLDER = "flask_app/static/uploads/"

app = Flask(__name__)
app.secret_key = vault.sec_key
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# print(vault.sec_key)