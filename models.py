from __init__ import db

class Assets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    asset_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300))
    serial_no = db.Column(db.String(10))
    serial_code = db.Column(db.String(10))
    colour = db.Column(db.String(10))
    date_bought = db.Column(db.String(10)) #yyyy-mm-dd format

    def __repr__(self):
        return "<Asset '{}': '{}' >".format(self.name, self.serial_code)

class SuperAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String)

    def __repr__(self):
        return '<Super Admin: %r>' %self.username

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String)

    def __repr__(self):
        return '<Admin: %r>' %self.username

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String)

    def __repr__(self):
        return '<User: %r>' %self.username

class Cases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_description = db.Column(db.String(300))
    case_item = db.Column(db.String(10))
    case_type = db.Column(db.String(10))

    def __repr__(self):
        return '<Case: %r>' %self.case_type
