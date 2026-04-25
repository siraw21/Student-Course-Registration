from models import User
from extensions import db


def register_user(username, email, password, role = 'student'):   
   user = User.query.filter_by(full_name = username).first()
   if user:
            return None
   else:
        new_user = User(full_name = username, role = role, email = email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        return new_user


def login_user(username, password):
     user = User.query.filter_by(full_name=username).first()

     if user and user.check_password(password):
       return user
     
     return None

def get_current_user(id):
     user = User.query.filter_by(id = id).first()
     return user


