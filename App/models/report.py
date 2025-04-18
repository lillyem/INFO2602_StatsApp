from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy.sql import func

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    year = db.Column(db.String(4), nullable=False)
    campus = db.Column(db.String(50), nullable=False)
    report_type = db.Column(db.String(100), nullable=False)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())

    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #admin_name = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    datafile_id = db.Column(db.Integer, db.ForeignKey('data_file.id'), nullable=False)

    charts = db.relationship('Chart', backref='report', lazy=True)

    def get_charts(self):
        return self.charts  

    def __init__(self, title, year, campus, report_type, admin_id, datafile_id, description=""):
        self.title = title
        self.year = year
        self.campus = campus
        self.report_type = report_type
        self.description = description
        self.admin_id = admin_id
        self.datafile_id = datafile_id

    def get_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "year": self.year,
            "campus": self.campus,
            "report_type": self.report_type,
            "published": self.published,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "admin_id": self.admin_id,
            "datafile_id": self.datafile_id
        }

    def __repr__(self):
        return f'<Report {self.id} - {self.title}>'
