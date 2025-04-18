from .user import create_user, create_admin
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bob@example.com', 'bobpass')
    create_admin('1234', 'sam','sam@mail.com', 'sampass' )


