from flask import Flask

#configure app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '\xcd\xefg\xb3\x08\x88\xdc1\xab\x96\x1cE\t\xd4\x17\xbf\xa7\x8b\xa3 B\xe3\xac\x9a'

import views