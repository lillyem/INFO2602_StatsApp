from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy.sql import func

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

