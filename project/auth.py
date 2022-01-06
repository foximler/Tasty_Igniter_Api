from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User, ApiKey
from .api import generate_api_key, get_active_orders, update_order_status, update_print_status
auth = Blueprint('auth', __name__)



################
# User Pages and methods
@auth.route('/login')
def login():
    return render_template('login.html')
@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
   
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user,remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#########################
# API key management functions
#
#
@auth.route('/signup')
@login_required
def signup():
    return render_template('signup.html', name=current_user.name)

@auth.route('/signup', methods=['POST'])
@login_required 
def signup_post():
    # code to validate and add Api Key to database
    email = current_user.email
    name = request.form.get('name')
    api_key = ApiKey.query.filter_by(name=name).first() # if this returns a key then the name already exists.
    if api_key: # if a user is found, we want to tell the user we cant copy names and make them restart
        flash('Name Already In use')
        return redirect(url_for('auth.signup'))

    # create a new api key with current users email, form given name and api_key function.
    new_api_key = ApiKey(email=email, name=name,api_key = generate_api_key())

    # add the new key to the database
    db.session.add(new_api_key)
    db.session.commit()

    return redirect(url_for('main.profile'))

@auth.route('/delete_api_key', methods=['POST'])
@login_required
def delete_api_key():
    api_key = bytes(request.form.get('api_key'),'utf-8')
    for_deletion = ApiKey.query.filter_by(api_key=api_key).one()
    db.session.delete(for_deletion)
    db.session.commit()
    return redirect(url_for('main.profile'))



###############################
#  Api Calls. All references too api.py file
#
#

@auth.route('/api/active_orders', methods=['POST'])
def api_get_active():
    api_key = bytes(request.form.get('api_key'),'utf-8')
    user = (ApiKey.query.filter_by(api_key=api_key).first())
    if user:
        api_return = get_active_orders()
        return jsonify(api_return)
    return "error"



@auth.route('/api/update_order_status', methods=['POST'])
def api_update_order_status():
    api_key = bytes(request.form.get('api_key'),'utf-8')
    order_id = request.form.get('order_id')
    order_status = request.form.get('order_status')
    user = ApiKey.query.filter_by(api_key=api_key)
    if user:
        update_order_status(order_id, order_status)
    return "0"



@auth.route('/api/update_print_status', methods=['POST'])
def api_update_print_status():
    api_key = bytes(request.form.get('api_key'),'utf-8')
    order_id = request.form.get('order_id')
    print_status = request.form.get('print_status')
    user = ApiKey.query.filter_by(api_key=api_key)
    if user:
        update_print_status(order_id, print_status)
    return "0"


