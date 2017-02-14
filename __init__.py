from flask import Flask

#configure app
app = Flask(__name__)
app.config['DEBUG'] = True

import views