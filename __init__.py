from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))

#configure app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '\xcd\xefg\xb3\x08\x88\xdc1\xab\x96\x1cE\t\xd4\x17\xbf\xa7\x8b\xa3 B\xe3\xac\x9a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'inventory.db')

#set up db
db = SQLAlchemy(app)

import views
import models