from models.enrollment import Enrollment
from models.course import Course
from extensions import db


def enroll_course(course_id, student_id):
  existing = Enrollment.query.filter_by(course_id = course_id, student_id = student_id).first()

  if existing:
     return None
  else:
     enrollment = Enrollment(course_id = course_id, student_id = student_id)
     db.session.add(enrollment)
     db.session.commit()
     return enrollment
  
def list_enrollment_courses():
    courses = Course.query.all()
    return courses

def list_enrolled_courses(user):
     if user.role == 'admin':
         return Enrollment.query.all()
     else: 
         return Enrollment.query.filter_by(student_id = user.id).all()
   
   