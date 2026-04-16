from extensions import db
from sqlalchemy.sql import func

class Course(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(50), nullable=False)
     code = db.Column(db.String(20), nullable=False)

     created_At = db.Column(db.DateTime, server_default=func.now())

     def to_dict(self):
        return {
           "id": self.id,
           "title": self.title,
           "code": self.code
        }

     def __repr__(self):
       return f"Title : {self.title}, Code: {self.code}" 