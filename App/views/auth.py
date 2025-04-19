from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.models import User

from.index import index_views

from App.controllers import (
    login
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    
@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')


@index_views.route('/')
def home_page():
    return render_template('index.html')


""" @auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    response = redirect(url_for('index_views.home_page'))
    if not token:
        flash('Bad username or password given'), 401
        return redirect(url_for('auth_views.login_page'))
    else:
        flash('Login Successful')
        set_access_cookies(response, token) 
    return response """
@auth_views.route('/login', methods=['POST'])
def login_action():
   data = request.form
   token = login(data['username'], data['password'])
  
   if not token:
       flash('Bad username or password given')
       return redirect(url_for('auth_views.login_page'))

   # Get user object from DB to check type
   user = User.query.filter_by(username=data['username']).first()


   if user and user.user_type == 'admin':
      response = redirect(url_for('admin_views.admin_home'))  # change this line
      set_access_cookies(response, token)
      flash('Login Successful')
      return response
  
   response = redirect(url_for('index_views.home_page'))  # Default redirect
   set_access_cookies(response, token)
   flash('Login Successful')
   return response





@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('auth_views.login_page')) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    data = request.form

    if not data.get('terms'):
        flash('You must agree to the Terms and Conditions to sign up.')
        return redirect(url_for('auth_views.signup_page'))
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    staff_id = data.get('staff_id')

    from App.controllers.user import create_user, create_admin  # make sure this import works

    if staff_id:
        user = create_admin(staff_id, username, email, password)
        user_type = 'admin'
    else:
        user = create_user(username, email, password)
        user_type = 'user'

    if user:
        flash(f'{user_type.capitalize()} account created successfully. You can log in now!')
        return redirect(url_for('auth_views.login_page'))
    else:
        flash('Username already or Staff ID exists. Try another one.')
        return redirect(url_for('auth_views.signup_page'))
'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/api/signup', methods=['POST'])
def signup_api():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('type', 'user')

    from App.controllers.user import create_user

    user = create_user(username, email, password)

    if user:
        return jsonify({'message': 'Account created successfully.'}), 201
    else:
        return jsonify({'message': 'Username already exists.'}), 409