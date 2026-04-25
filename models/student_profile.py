from extensions import db
from sqlalchemy.sql import func

class Student_Profile(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     student_id = db.Column(db.String(30), nullable=False, unique=True)
     department = db.Column(db.String(60), nullable=False, default="Software Engineering")
     year = db.Column(db.Integer, nullable=False)

     created_At = db.Column(db.DateTime, server_default=func.now())
     


     def to_dict(self):
        return {
           "id": self.id,
           "User Id": self.user_id,
           "Student Id": self.student_id,
           "Department": self.department,
           "Year": self.year,
        }

     def __repr__(self):
       return f"Student Id : {self.student_id}, Department: {self.department}, Year: {self.year}," 