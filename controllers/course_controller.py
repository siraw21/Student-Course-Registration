from flask import Blueprint, render_template, request, redirect, url_for, session
from services.course_service import add_course, list_all_courses
from forms.course_forms import CourseDetailForm

course_bp = Blueprint('courses', __name__)

@course_bp.route("/new_course", methods=['GET','POST'])
def create_course():
   if 'user_id' not in session:
        return redirect(url_for('auth.login'))
   if session['role'] == 'admin':
         form = CourseDetailForm()
         if form.validate_on_submit():
            title = form.title.data
            code = form.code.data
            credit_hours = form.credit_hours.data
            description = form.description.data
            category = form.category.data
            instructor_name = form.instructor_name.data
            required_year = form.required_year.data
            
            course = add_course(title, code, credit_hours, description, category, instructor_name, required_year)
            # Course logic
            
            if course:
              return redirect(url_for('main.dashboard'))
            else:
               return "sth is wrong"
         else:
            return render_template('create_course.html', form = form)   
   else:
      return redirect(url_for('auth.logout'))


@course_bp.route("/courses")
def list_course():
   if 'user_id' not in session:
        return redirect(url_for('auth.login'))
   courses = list_all_courses()
   result = [course.to_dict() for course in courses]
     
   if result:    
     return render_template('list_course.html', result=result)
   else:
     return "no available course"