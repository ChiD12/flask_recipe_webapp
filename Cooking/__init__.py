from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

import os


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '34HBHB3245JN3434JKDFD8W77HBGTF777HSYG3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "SOEN287Recipe@gmail.com"            #os.environmen.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = "pasSword123"                        #os.environmen.get('EMAIL_PASSWORD')
#user is SOEN287Recipe@gmail.com
#pass is pasSword123
mail = Mail(app)

from Cooking import routes
