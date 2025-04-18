import os
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_admin import Admin
from App.models import db, User
from App.models.datafile import DataFile
from App.models.report import Report
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
        # Retrieve form fields
        year = request.form.get('year')
        campus = request.form.get('campus')
        report_type = request.form.get('report')
        file = request.files.get('report')

        # Basic validation
        if not (year and campus and report_type and file):
            flash('All fields are required.')
            return redirect(url_for('admin_views.upload_report'))

        if file and allowed_file(file.filename):
            # Ensure the folder exists
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Save to DB
            datafile = DataFile(filename=filename, admin_id=current_user.id)
            db.session.add(datafile)
            db.session.commit()

            report = Report(
                title=request.form.get('title'),
                description=request.form.get('description', ''),
                year=int(request.form.get('year')),
                campus=request.form.get('campus'),
                report_type=request.form.get('report'),
                admin_id=current_user.id,
                datafile_id=datafile.id
            )
            db.session.add(report)
            db.session.commit()

            flash('Report uploaded and saved successfully.')
            return redirect(url_for('admin_views.upload_report'))
        else:
            flash('Invalid file type. Please upload PDF, CSV, or XLSX.')
            return redirect(url_for('admin_views.upload_report'))

    return render_template('admin/upload.html', is_authenticated=True)



@admin_views.route('/admin/reports', methods=['GET'])
@jwt_required()
def view_reports():
    try:
        verify_jwt_in_request()

        # Get filter parameters from the query string
        year = request.args.get('year')
        campus = request.args.get('campus')
        category = request.args.get('category')  # report_type

        # Base query
        query = Report.query

        if year:
            query = query.filter_by(year=year)
        if campus:
            query = query.filter_by(campus=campus)
        if category:
            query = query.filter_by(report_type=category)

        reports = query.all()

        enriched_reports = []
        for report in reports:
            datafile = report.datafile
            enriched_reports.append({
                'title': report.title,
                'description': report.description,
                'campus': report.campus,
                'report_type': report.report_type,
                'year': report.year,
                'filename': datafile.filename,
                'filepath': os.path.join('static', 'reports', datafile.filename),
                'uploaded_by': report.admin_id,
                'created_at': report.created_at.strftime('%Y-%m-%d %H:%M'),
            })

        return render_template(
            'view_reports.html',
            reports=enriched_reports,
            selected_year=year,
            selected_campus=campus,
            selected_category=category,
            is_authenticated=True
        )

    except Exception as e:
        flash('Please log in to view reports.')
        return redirect(url_for('auth_views.login_page')) 
 
