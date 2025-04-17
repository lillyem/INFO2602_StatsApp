from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy.sql import func

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())

    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datafile_id = db.Column(db.Integer, db.ForeignKey('data_file.id'), nullable=False)

    charts = db.relationship('Chart', backref='report', lazy=True)

    def get_charts(self):
        return self.charts  

    def __init__(self, title, admin_id, datafile_id, description=""):
        self.title = title
        self.description = description
        self.admin_id = admin_id
        self.datafile_id = datafile_id

    def get_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "published": self.published,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "admin_id": self.admin_id,
            "datafile_id": self.datafile_id
        }

    def __repr__(self):
        return f'<Report {self.id} - {self.title}>'
