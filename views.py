from __init__ import app, db
from flask import render_template, url_for, request, redirect, flash
from forms import LoginForm
from models import *

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
        return redirect(request.args.get('next') or url_for('super_admin'))
    return render_template('super_admin_login.html', form = form)


@app.route('/admin_login', methods = ["GET", "POST"])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash("Signed in successfully as {}".format(username))
        return redirect(request.args.get('next') or url_for('home'))
    return render_template('admin_login.html', form = form)


@app.route('/user_login', methods = ["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash("Signed in successfully as {}".format(username))
        return redirect(request.args.get('next') or url_for('home'))
    return render_template('user_login.html', form = form)


@app.route('/super_admin', methods = ["GET", "POST"])
def super_admin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db.session.add(Admin(username=username, password_hash=password))
        db.session.commit()
        flash("Successfully created {} as Admin".format(username))
        return redirect(request.args.get('next') or url_for('super_admin'))
    return render_template('super_admin.html', form = form)

