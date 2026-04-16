from models.course import Course
from extensions import db

def add_course(title, code):
  if title and code :
      course = Course(title = title, code = code)

      db.session.add(course)
      db.session.commit()
      return course
  else:
     return None

def list_all_courses():
   courses = Course.query.all()
   return courses   