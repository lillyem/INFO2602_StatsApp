from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy.sql import func


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
    