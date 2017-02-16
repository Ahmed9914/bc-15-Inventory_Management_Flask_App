from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))

#configure app
app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '\xcd\xefg\xb3\x08\x88\xdc1\xab\x96\x1cE\t\xd4\x17\xbf\xa7\x8b\xa3 B\xe3\xac\x9a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory_db.db')

#set up db
db = SQLAlchemy(app)

#configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "home"
login_manager.init_app(app)

import views
import models
