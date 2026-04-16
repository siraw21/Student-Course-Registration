from flask import Blueprint, render_template, request, redirect, url_for, session
from services.course_service import add_course, list_all_courses

course_bp = Blueprint('courses', __name__)

@course_bp.route("/new_course", methods=['GET','POST'])
def create_course():
   if session['role'] == 'admin':
         if request.method == 'POST':
            title = request.form.get('title')
            code = request.form.get('code')
            
            course = add_course(title, code)
            # Course logic
            
            if course:
              return redirect(url_for('main.dashboard'))
            else:
               return "sth is wrong"
         else:
            return render_template('create_course.html')   
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