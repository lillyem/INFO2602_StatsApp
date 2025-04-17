from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy.sql import func


class DataFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, default=func.now())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    reports = db.relationship('Report', backref='datafile', lazy=True)

    def __init__(self, filename, admin_id):
        self.filename = filename
        self.admin_id = admin_id

    def get_json(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "upload_time": self.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            "admin_id": self.admin_id
        }

    def __repr__(self):
        return f'<DataFile {self.id} - {self.filename}>'

