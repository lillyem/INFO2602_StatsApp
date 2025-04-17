from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50)) 

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'type': self.type
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.id} - {self.username}>'
    

class Admin(User):
    __tablename__ = 'admin'
    staff_id = db.Column(db.String(120), unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    datafiles = db.relationship('DataFile', backref='admin', lazy=True)
    reports = db.relationship('Report', backref='admin', lazy=True)

    def __init__(self, staff_id, username, email, password):
        super().__init__(username, email, password)
        self.staff_id = staff_id

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "staff_id": self.staff_id,
            "type": self.type
        }

    def __repr__(self):
        return f'<Admin {self.id} - {self.username}>'



# class DataFile(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # filename = db.Column(db.String(255), nullable=False)
    # upload_time = db.Column(db.DateTime, default=func.now())
    # admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # reports = db.relationship('Report', backref='datafile', lazy=True)

    # def __init__(self, filename, admin_id):
    #     self.filename = filename
    #     self.admin_id = admin_id

    # def get_json(self):
    #     return {
    #         "id": self.id,
    #         "filename": self.filename,
    #         "upload_time": self.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
    #         "admin_id": self.admin_id
    #     }

    # def __repr__(self):
    #     return f'<DataFile {self.id} - {self.filename}>'

class EnrollmentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False)
    course_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(100))
    semester = db.Column(db.String(50))
    year = db.Column(db.Integer)
    num_students = db.Column(db.Integer)

    datafile_id = db.Column(db.Integer, db.ForeignKey('data_file.id'), nullable=False)

    def get_json(self):
        return {
            "id": self.id,
            "course_code": self.course_code,
            "course_name": self.course_name,
            "department": self.department,
            "semester": self.semester,
            "year": self.year,
            "num_students": self.num_students,
            "datafile_id": self.datafile_id
        }
    
# class Report(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     published = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=func.now())

#     admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     datafile_id = db.Column(db.Integer, db.ForeignKey('data_file.id'), nullable=False)

#     charts = db.relationship('Chart', backref='report', lazy=True)

#     def __init__(self, title, admin_id, datafile_id, description=""):
#         self.title = title
#         self.description = description
#         self.admin_id = admin_id
#         self.datafile_id = datafile_id

#     def get_json(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "description": self.description,
#             "published": self.published,
#             "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#             "admin_id": self.admin_id,
#             "datafile_id": self.datafile_id
#         }

#     def __repr__(self):
#         return f'<Report {self.id} - {self.title}>'



class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    chart_type = db.Column(db.String(50), nullable=False) 
    data = db.Column(db.Text, nullable=False) 
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)

    def __init__(self, title, chart_type, data, report_id):
        self.title = title
        self.chart_type = chart_type
        self.data = data
        self.report_id = report_id

    def get_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "chart_type": self.chart_type,
            "data": self.data,
            "report_id": self.report_id
        }

    def __repr__(self):
        return f'<Chart {self.id} - {self.title} ({self.chart_type})>'

