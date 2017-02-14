from __init__ import app
from flask import render_template, url_for, request, redirect, flash
from forms import LoginForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/super_admin_login', methods = ["GET", "POST"])
def super_admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash("Signed in successfully as {}".format(username))
        return redirect(request.args.get('next') or url_for('home'))
    return render_template('super_admin_login.html', form = form)
