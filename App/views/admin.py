from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_admin import Admin
from App.models import db, User
from flask import Blueprint, render_template, redirect, url_for, request, flash




admin_views = Blueprint('admin_views', __name__, template_folder='../templates/admin')


class AdminView(ModelView):


   @jwt_required()
   def is_accessible(self):
       return current_user and current_user.type == 'admin'


   def inaccessible_callback(self, name, **kwargs):
       # redirect to login page if user doesn't have access
       flash("Admin access only.")
       return redirect(url_for('auth_views.login_page'))


def setup_admin(app):
   admin = Admin(app, name='FlaskMVC', template_mode='bootstrap3')
   admin.add_view(AdminView(User, db.session))


@admin_views.route('/admin')
def admin_home():
   try:
       verify_jwt_in_request()
       if current_user and current_user.type == 'admin':
           return render_template('index.html', is_authenticated=True)
       else:
           flash("Admins only.")
           return redirect(url_for('auth_views.login_page'))
   except Exception:
       flash("Please log in as an admin.")
       return redirect(url_for('auth_views.login_page'))
  
""" @admin_views.route('/admin')
@jwt_required()
def admin_home():
       return render_template('index.html') """

