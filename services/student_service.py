from models import  Student_Profile
from extensions import db

def create_student_profile(user_id, student_id, year):
    new_student_profile = Student_Profile(user_id = user_id , student_id = student_id, year = year )

    db.session.add(new_student_profile)
    db.session.commit()
    return new_student_profile