from models.course import Course
from extensions import db

def add_course(title, code, credit_hours, description, category, instructor_name, required_year):
  if title and code :
      course = Course(title = title, code = code, credit_hours = credit_hours, description = description, category = category, instructor_name = instructor_name, required_year = required_year)

      db.session.add(course)
      db.session.commit()
      return course
  else:
     return None
  
def remove_course(code):
      pass

def list_all_courses():
   courses = Course.query.all()
   return courses   

def get_course(id):
   course = Course.query.get_or_404(id)
   return course

def populate_course_obj(form, course):
    try:
        form.populate_obj(course)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
    
def delete_course_service(course):
    try: 
        db.session.delete(course)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print("DELETE ERROR:", e) 
        return False    
    
