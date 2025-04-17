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

