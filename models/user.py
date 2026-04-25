from extensions import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     full_name = db.Column(db.String(150), nullable=False)
     role = db.Column(db.String(100), nullable=False, default="student")
     password_hash = db.Column(db.String(255), nullable=False)
     email = db.Column(db.String(250), nullable=False)
     created_At = db.Column(db.DateTime, server_default=func.now())
     
     student_profile = db.relationship('Student_Profile', backref='user', uselist=False)

     def set_password(self, password):
        self.password_hash = generate_password_hash(password)
     
     def check_password(self, password):
        return check_password_hash(self.password_hash, password)

     def __repr__(self):
       return f"Name : {self.username}, Role: {self.role}"