from App.models import User, Admin
from App.database import db

#def create_user(username, password):
 #   newuser = User(username=username, password=password)
  #  db.session.add(newuser)
   # db.session.commit()
    #return newuser

def create_user(username, email, password):
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return None
    newuser = User(username=username, email=email, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_admin(staff_id, username, email, password):
    if User.query.filter((User.username == username) | (User.email == email) | (Admin.staff_id == staff_id)).first():
        return None
    admin = Admin(staff_id=staff_id, username=username, email=email, password=password)
    db.session.add(admin)
    db.session.commit()
    return admin

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    