import os
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_admin import Admin
from App.models import db, User
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename


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
           return render_template('admin/admin_index.html', is_authenticated=True)
       else:
           flash("Admins only.")
           return redirect(url_for('auth_views.login_page'))
   except Exception:
       flash("Please log in as an admin.")
       return redirect(url_for('auth_views.login_page'))
   
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'App', 'static', 'reports')
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'xlsx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_views.route('/admin/upload', methods=['GET', 'POST'])
@jwt_required()
def upload_report():
   if not current_user or current_user.type != 'admin':
       flash('Admins only.')
       return redirect(url_for('auth_views.login_page'))

   if request.method == 'POST':
       file = request.files.get('report')
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(UPLOAD_FOLDER, filename))
           flash('Report uploaded successfully.')
           return redirect(url_for('admin_views.upload_report'))
       else:
           flash('Invalid file type. Please upload PDF, CSV, or XLSX.')

   return render_template('admin/upload.html', is_authenticated=True)

@admin_views.route('/admin/reports', methods=['GET'])
@jwt_required()
def view_reports():
    """ if not current_user or current_user.type != 'admin':
        flash('Admins only.')
        return redirect(url_for('auth_views.login_page')) """

    reports_dir = os.path.join(os.getcwd(), 'App', 'static', 'reports')
    reports = []

    if os.path.exists(reports_dir):
        for filename in os.listdir(reports_dir):
            if os.path.isfile(os.path.join(reports_dir, filename)):
                reports.append(filename)

    return render_template('view_reports.html', reports=reports, is_authenticated=True)

  
""" @admin_views.route('/admin')
@jwt_required()
def admin_home():
       return render_template('index.html') """

