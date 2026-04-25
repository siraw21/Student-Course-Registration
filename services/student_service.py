from models import  Student_Profile

from extensions import db

def create_student_profile(user_id, student_id, year):
    new_student_profile = Student_Profile(user_id = user_id , student_id = student_id, year = year )

    db.session.add(new_student_profile)
    db.session.commit()
    return new_student_profile

def get_student_profile(id):    
    student = Student_Profile.query.get_or_404(id)
    
    return student

def populate_student_obj(profile_form, student):
    try:
        profile_form.populate_obj(student)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
