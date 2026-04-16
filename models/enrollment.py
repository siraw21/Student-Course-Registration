from extensions import db
from sqlalchemy.sql import func

class Enrollment(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
     student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

     created_At = db.Column(db.DateTime, server_default=func.now())

     course = db.relationship('Course', backref='enrollments')
     student = db.relationship('User', backref='enrollments')
   

     def __repr__(self):
       return f"Course : {self.course_id}, Student: {self.student_id}"