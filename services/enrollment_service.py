from models.enrollment import Enrollment
from models.course import Course
from extensions import db


def enroll_course(course_id, student_id):
    existing = Enrollment.query.filter_by(
        course_id=course_id,
        student_id=student_id
    ).first()

    if existing:
        return None

    enrollment = Enrollment(
        course_id=course_id,
        student_id=student_id
    )

    db.session.add(enrollment)
    db.session.commit()

    return enrollment
  
def list_enrollment_courses(student_id):
    courses = Course.query.all()

    enrolled = Enrollment.query.filter_by(
        student_id=student_id
    ).all()

    enrolled_ids = {e.course_id for e in enrolled}

    result = []

    for course in courses:
        course_dict = course.to_dict()

        
        course_dict["is_enrolled"] = course.id in enrolled_ids

        result.append(course_dict)

    return result

def list_enrolled_courses(user):
     if user.role == 'admin':
         return Enrollment.query.all()
     else: 
         return Enrollment.query.filter_by(student_id = user.id).all()
   
   