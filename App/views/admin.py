import os
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_admin import Admin
from App.models import db, User
from App.models.datafile import DataFile
from App.models.report import Report
from App.models import Chart
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt


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
        claims = get_jwt()
        # print("JWT Claims >>>", claims)
        if claims.get('role') == "admin":
            return render_template('admin/admin_index.html', is_authenticated=True)
        else:
            flash("Admins only.")
            return redirect(url_for('auth_views.login_page'))
    except Exception as e:
        flash("Please log in as an admin.")
        return redirect(url_for('auth_views.login_page'))
   
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'App', 'static', 'reports')
ALLOWED_EXTENSIONS = {'pdf', 'csv', 'xlsx'}

CHART_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'App', 'static', 'charts')
CHART_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename, allowed_exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts


@admin_views.route('/admin/upload', methods=['GET', 'POST'])
@jwt_required()
def upload_report():
    if not current_user or current_user.user_type != 'admin':
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

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
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
#@jwt_required()
def view_reports():
    try:
            #verify_jwt_in_request()
            #current_user = get_jwt_identity()

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
                #is_authenticated=True
            )

    except Exception as e:
            flash('Please log in to view reports.')
            return redirect(url_for('auth_views.login_page')) 
    
    
@admin_views.route('/admin/upload-chart', methods=['GET', 'POST'])
@jwt_required()
def upload_chart():
    if not current_user or current_user.user_type != 'admin':
        flash('Admins only.')
        return redirect(url_for('auth_views.login_page'))

    if request.method == 'POST':
        # Retrieve form fields
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('chart')
        chart_type = request.form.get('chart_type') 

        # Basic validation
        if not (title and chart_type and file):
            flash('Title and chart file are required.')
            return redirect(url_for('admin_views.upload_chart'))

        # Allowed image extensions
        allowed_extensions = {'png', 'jpg', 'jpeg'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

        if file and allowed_file(file.filename):
            if not os.path.exists(CHART_UPLOAD_FOLDER):
                os.makedirs(CHART_UPLOAD_FOLDER)

            filename = secure_filename(file.filename)
            file_path = os.path.join(CHART_UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Save to DB (optional: link to chart model or just store the path)
            """ datafile = DataFile(filename=filename, admin_id=current_user.id)
            db.session.add(datafile)
            db.session.commit() """

            # Optional: Save metadata as report/chart
            chart = Chart(
                title=title,
                chart_type=chart_type,
                data=description,
                image = filename
            )
            db.session.add(chart)
            db.session.commit()


            flash('Chart image uploaded and saved successfully.')
            return redirect(url_for('admin_views.upload_chart'))
        else:
            flash('Invalid file type. Please upload PNG or JPEG images.')
            return redirect(url_for('admin_views.upload_chart'))

    return render_template('admin/upload_chart.html', is_authenticated=True)

@admin_views.route('/admin/charts', methods=['GET'])
def view_charts():
    # Optional filters via query string
    try:
        chart_type = request.args.get('chart_type')
        title = request.args.get('title')

        query = Chart.query

        if chart_type:
            query = query.filter_by(chart_type=chart_type)
        if title:
            query = query.filter(Chart.title.ilike(f"%{title}%"))

        charts = query.all()

        chart_list = []
        for chart in charts:
            chart_list.append({
                'id': chart.id,
                'title': chart.title,
                'chart_type': chart.chart_type,
                'data': chart.data,
                'image':chart.image
            })

        return render_template(
            'charts.html',
            charts=chart_list,
            selected_type=chart_type,
            search_title=title
        )
    except Exception as e:
        flash('Please log in to view reports.')
        return redirect(url_for('auth_views.login_page')) 

@admin_views.route('/admin/delete-chart/<int:chart_id>', methods=['POST'])
@jwt_required()
def delete_chart(chart_id):
    try:
        chart = Chart.query.get(chart_id)

        if not chart:
            flash('Chart not found.')
            return redirect(url_for('admin_views.view_charts'))

        # Remove image file if it exists
        if chart.image:
            image_path = os.path.join(CHART_UPLOAD_FOLDER, chart.image)
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(chart)
        db.session.commit()

        flash('Chart deleted successfully.')
        return redirect(url_for('admin_views.view_charts'))

    except Exception as e:
        flash('An error occurred while deleting the chart.')
        print(f"[ERROR] Delete chart: {e}")
        return redirect(url_for('admin_views.view_charts'))

@admin_views.route('/charts/update-title/<int:chart_id>', methods=['POST'])
@jwt_required()
def update_chart_title(chart_id):
    try:
        chart = Chart.query.get(chart_id)

        new_title = request.form.get('title')

        if new_title:
            chart.title = new_title
            db.session.commit()
            flash('Chart title updated successfully.', 'success')
        else:
            flash('Please enter a new title.', 'warning')

        return redirect(url_for('admin_views.view_charts'))
    except Exception as e:
        flash('An error occurred while changing the name.')
        print(f"[ERROR] Delete chart: {e}")
        return redirect(url_for('admin_views.view_charts'))