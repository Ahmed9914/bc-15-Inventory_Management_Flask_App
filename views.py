from __init__ import app, db, login_manager
from flask import render_template, url_for, request, redirect, flash
from forms import *
from models import *
from flask_login import login_required, login_user,logout_user, current_user
from datetime import datetime, timedelta


current_user_type = ""

def reclaim():
    date = datetime.now()
    allowance = date + timedelta(3)
    reclaim_list = Assets.query.filter(Assets.reclaim_date < allowance).all()
    return reclaim_list


def resolve_case(arg):
    entry = Cases.query.filter_by(asset_name=arg).first()
    print(entry)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('list_cases'))

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
    assets_due = reclaim()
    if form.validate_on_submit():
        current_user_type = 'Admin'
        username = form.username.data
        user = Admins.get_by_username(username)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            if user.username == 'sAdmin':
                return redirect(request.args.get('next') or url_for('super_admin'))
            else:
                if assets_due is not None:

                    flash("THERE ARE NEW ASSETS TO BE RECLAIMED SOON")
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
        a1 = Assets(asset_name='MACBOOK-01', description='LAPTOP COMPUTER',
                                serial_no='12345', serial_code='AND-L',
                                colour='WHITE', date_bought='2016-12-03')
        a2 = Assets(asset_name='MACBOOK-03', description='LAPTOP COMPUTER',
                                serial_no='92365', serial_code='AND-L',
                                colour='BLACK', date_bought='2015-12-05')
        a3 = Assets(asset_name='MACBOOK-02', description='LAPTOP COMPUTER',
                                serial_no='90645', serial_code='AND-L',
                                date_bought='2015-07-03')
        a4 = Assets(asset_name='MACBOOK-03', description='LAPTOP COMPUTER',
                                serial_no='023345', serial_code='AND-L',
                                colour='WHITE', date_bought='2014-02-05')
        a5 = Assets(asset_name='ROUTER', description='WIRELESS ROUTER',
                                serial_no='90972', serial_code='AND-R',
                                date_bought='2015-05-14')
        a6 = Assets(asset_name='SONY TV', description='FLAT SCREEN TV',
                                serial_no='812472', serial_code='AND-T',
                                date_bought='2016-12-14')
        db.session.add(a1)
        db.session.add(a2)
        db.session.add(a3)
        db.session.add(a4)
        db.session.add(a5)
        db.session.add(a6)
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
        if not User.query.filter_by(username=user_name).first():
            db.session.add(User(username=user_name, first_name=first_name,
                                last_name=last_name))
            db.session.commit()
            flash("Successfully added {} to Users".format(user_name))
            return redirect(url_for('admin'))
        else:
            flash("{} already exists".format(user_name))
            return redirect(url_for('admin'))
    return render_template('add_user.html', form = form)


@app.route("/sign_out")
def sign_out():
    logout_user()
    return redirect(url_for('home'))


@app.route('/user', methods=["GET", "POST"])
@login_required
def user():
    form = CaseForm()
    if form.validate_on_submit():
        asset_name = form.asset_name.data
        asset = Assets.query.filter_by(asset_name=asset_name).first()
        if asset is not None:
            if asset.user_assigned is not None:
                if form.report_lost.data:
                    db.session.add(Cases(asset_name=asset_name,
                                         case_type="LOST", reported_by=current_user.username))
                    c1 = Cases(asset_name='SONY TV',
                                         case_type="LOST", reported_by=current_user.username)

                    c2 = Cases(asset_name='MACBOOK-02',
                                         case_type="LOST", reported_by=current_user.username)
                    c3 = Cases(asset_name='MACBOOK-03',
                                         case_type="LOST", reported_by=current_user.username)
                    db.session.add(c1)
                    db.session.add(c2)
                    db.session.add(c3)
                    db.session.commit()
                    asset.status = 'LOST'
                    db.session.commit()
                    flash("Your case of LOST {} has been recorded".format(asset_name))
                    return redirect(url_for('user'))

                elif form .report_found.data:
                    if asset.status == 'LOST':
                        db.session.add(Cases(asset_name=asset_name,
                                             case_type="FOUND", reported_by=current_user.username))
                        c4 = Cases(asset_name='IPHONE',
                                             case_type="FOUND", reported_by=current_user.username)
                        db.session.add(c4) 
                        db.session.commit()
                        asset.status = 'FOUND'
                        db.session.commit()
                        flash("Your case of FOUND {} has been recorded".format(asset_name))
                        return redirect(url_for('user'))
                    else:
                        flash("{} HAS NOT BEEN REPORTED AS LOST".format(asset_name))
                        return redirect(url_for('user'))
            else:
                flash("{} IS NOT YET ASSIGNED".format(asset_name))
                return redirect(url_for('user'))
        else:
            flash("{} DOESNT EXIST".format(asset_name))
            return redirect(url_for('user'))
    return render_template("user.html", form=form)


@app.route('/admin/assign_asset', methods = ["GET", "POST"])
@login_required
def assign_asset():
    form = AssignForm()
    if form.validate_on_submit():
        asset_name = form.asset_name.data
        user_assigned = form.user_assigned.data
        reclaim_date = form.reclaim_date.data
        asset = Assets.query.filter_by(asset_name=asset_name).first()
        user = User.get_by_username(user_assigned)
        if user is not None and asset is not None:
            if asset.user_assigned is not None:
                flash("ERROR!! {} is already assigned to some one else".format(asset_name, asset.user_assigned ))
                return redirect(url_for('admin'))
            else:
                asset.user_assigned = user_assigned
                asset.reclaim_date = reclaim_date
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
        if asset.status == 'LOST':
            asset_name = asset.asset_name + '*'
        elif asset.status == 'FOUND':
            asset_name = asset.asset_name + '***'
        else:
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


@app.route('/admin/list_cases', methods=["GET", "POST"])
@login_required
def list_cases():
    form = ResolveForm()
    result = []
    list_cases = Cases.query.all()
    for case in list_cases:       
        asset_name = case.asset_name
        case_type = case.case_type
        reported_by = case.reported_by        
        result.append([asset_name, case_type, reported_by])
        if form.resolve.data:
            resolve_case(asset_name)
            flash("Case Resolved Successfully")
            return redirect(url_for('list_cases'))
    return render_template('list_cases.html', lst=result, form=form)