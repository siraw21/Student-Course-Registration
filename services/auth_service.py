from models.user import User
from extensions import db


def register_user(username, password, role = 'student'):   
   user = User.query.filter_by(username = username).first()
   if user:
            return None
   else:
        new_user = User(username = username, role = role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        return new_user


def login_user(username, password):
     user = User.query.filter_by(username=username).first()

     if user and user.check_password(password):
       return user
     
     return None


