from extensions import db
from sqlalchemy.sql import func

class Course(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(50), nullable=False)
     code = db.Column(db.String(20), unique=True ,nullable=False)
     credit_hours = db.Column(db.Integer, nullable=False)
     description = db.Column(db.String(250), nullable=False)
     category = db.Column(db.String(150), nullable=True)
     required_year = db.Column(db.Integer, nullable=False)
     instructor_name = db.Column(db.String(150), nullable=False)

     created_At = db.Column(db.DateTime, server_default=func.now())

     def to_dict(self):
        return {
           "id": self.id,
           "title": self.title,
           "code": self.code,
           "credit_hours": self.credit_hours,
           "description": self.description,
           "category": self.category,
           "required_year": self.required_year,
           "instructor_name": self.instructor_name,
           "created_At": self.created_At
        }

     def __repr__(self):
       return f"Title : {self.title}, Code: {self.code}" 