from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()] )
    submit = SubmitField('Sign In: ')
    create = SubmitField('Create Account: ')

class AssetForm(Form):
    asset_name = StringField('Asset name: ', validators=[DataRequired()])
    description = StringField('Asset description: ', validators=[DataRequired()])
    serial_no = StringField('Serial Number: ', validators=[DataRequired()])
    serial_code = StringField('Serial Code: ', validators=[DataRequired()])
    date_bought = StringField('Bought on: ', validators=[DataRequired()])
    colour = StringField('Color(optional): ')
    add = SubmitField('Add asset: ')

