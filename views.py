from __init__ import app, db, login_manager
from flask import render_template, url_for, request, redirect, flash
from forms import LoginForm, AssetForm, UserForm, AssignForm
from models import *
from flask_login import login_required, login_user,logout_user, current_user

current_user_type = ""

@login_manager.user_loader
def load_user(userid):
    if current_user_type == 'Admin':
        return Admins.query.get(int(userid))
    elif current_user_type == 'User':
        return User.query.get(int(userid))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/admins_login', methods = ["GET", "POST"])
def admins_login():
    global current_user_type
    form = LoginForm()
    if form.validate_on_submit():
        current_user_type = 'Admin'
        username = form.username.data
        user = Admins.get_by_username(username)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("Signed in successfully as {} ".format(username))
            if user.username == 'sAdmin':
                return redirect(request.args.get('next') or url_for('super_admin'))
            else:
                return redirect(request.args.get('next') or url_for('admin'))
            
        flash("Wrong username or password")
    return render_template('admins_login.html', form = form)


@app.route('/user_login', methods = ["GET", "POST"])
def user_login():
    global current_user_type
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.get_by_username(username)
        if user is not None:
            login_user(user)       
            flash("Signed in successfully as {} ".format(username))
            current_user_type = 'User'
            return redirect(request.args.get('next') or url_for('user'))
        flash("Wrong username")
    return render_template('user_login.html', form = form)


@app.route('/super_admin', methods = ["GET", "POST"])
@login_required
def super_admin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db.session.add(Admins(username=username, password=password))
        db.session.commit()
        flash("Successfully created {} as Admin".format(username))
        return redirect(request.args.get('next') or url_for('super_admin'))
    return render_template('super_admin.html', form = form)


@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html")


@app.route('/admin/add_asset', methods = ["GET", "POST"])
@login_required
def add_asset():
    form = AssetForm()
    if form.validate_on_submit():
        asset_name = form.asset_name.data
        description = form.description.data
        serial_no = form.serial_no.data
        serial_code = form.serial_code.data
        colour = form.colour.data
        date_bought = form.date_bought.data
        db.session.add(Assets(asset_name=asset_name, description=description,
                                serial_no=serial_no, serial_code=serial_code,
                                colour=colour, date_bought=date_bought))
        db.session.commit()
        flash("Successfully added {} to the records".format(asset_name))
        return redirect(url_for('admin'))
    return render_template('add_asset.html', form = form)


@app.route('/admin/add_user', methods = ["GET", "POST"])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user_name = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        db.session.add(User(username=user_name, first_name=first_name,
                            last_name=last_name))
        db.session.commit()
        flash("Successfully added {} to Users".format(user_name))
        return redirect(url_for('admin'))
    return render_template('add_user.html', form = form)


@app.route("/sign_out")
def sign_out():
    logout_user()
    flash("You have now signed out")
    return redirect(url_for('home'))


@app.route('/user')
@login_required
def user():
    return render_template("user.html")


@app.route('/admin/assign_asset', methods = ["GET", "POST"])
@login_required
def assign_asset():
    form = AssignForm()
    if form.validate_on_submit():
        asset_name = form.asset_name.data
        user_assigned = form.user_assigned.data
        asset = Assets.query.filter_by(asset_name=asset_name).first()
        user = User.get_by_username(user_assigned)
        if user is not None and asset is not None:
            if asset.user_assigned is not None:
                flash("ERROR!! {} is already assigned to some one else".format(asset_name, asset.user_assigned ))
                return redirect(url_for('admin'))
            else:
                asset.user_assigned = user_assigned
                db.session.commit()
                flash("Successfully assigned {} to {}".format(asset_name, user_assigned))
                return redirect(url_for('admin'))
        else:
            flash("{} or  {} does not exist".format(asset_name, user_assigned))
            return redirect(url_for('assign_asset'))
    return render_template('assign_asset.html', form = form)

@app.route('/admin/unassign_asset', methods = ["GET", "POST"])
@login_required
def unassign_asset():
    form = AssignForm()
    if form.validate_on_submit():
        asset_name = form.asset_name.data
        asset = Assets.query.filter_by(asset_name=asset_name).first()
        if asset is not None:
            user_assigned = asset.user_assigned
            if user_assigned is not None:
                asset.user_assigned = None
                db.session.commit()
                flash("Successfully unassigned {} from {}".format(asset_name, user_assigned))
                return redirect(url_for('admin'))
            else:
                flash("ERROR!!! {} is not yet asigned".format(asset_name))
                return redirect(url_for('unassign_asset'))
        else:
            flash("ERROR!! {} does not exist".format(asset_name))
            return redirect(url_for('unassign_asset'))
    return render_template('unassign_asset.html', form = form)


@app.route('/admin/list_assigned')
@login_required
def list_assigned():
    result = []
    list_assigned = Assets.query.filter(Assets.user_assigned != None)
    for asset in list_assigned:
        asset_name = asset.asset_name
        user_assigned = asset.user_assigned
        result.append([asset_name, user_assigned])
    return render_template('list_assigned.html', lst=result)


@app.route('/admin/list_unassigned')
@login_required
def list_unassigned():
    result = []
    list_unassigned = Assets.query.filter(Assets.user_assigned == None)
    for asset in list_unassigned:
        asset_name = asset.asset_name
        description = asset.description
        result.append([asset_name, description])
    return render_template('list_unassigned.html', lst=result)



