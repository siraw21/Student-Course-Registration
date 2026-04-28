from flask import Blueprint, render_template, flash, redirect, url_for, session
from services.course_service import add_course, list_all_courses, get_course, populate_course_obj, delete_course_service
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
   
   if session.get('role') != 'admin':
        return "Unauthorized", 403
   courses = list_all_courses()
   result = [course.to_dict() for course in courses]
     
   if result:    
     return render_template('list_course.html', result=result)
   else:
     return "no available course"
   

@course_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit_course(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    course = get_course(id)
    form = CourseDetailForm(obj=course)

    if form.validate_on_submit():
      result = populate_course_obj(form, course)
      if result:
            flash("Course updated successfully!", "success")
            return redirect(url_for('courses.list_course'))
      else:
         flash("Error updating course", "danger")
    return render_template('edit_course.html', form=form, course = course)

@course_bp.route("/delete/<int:id>", methods=['POST'])
def delete_course(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if session.get('role') != 'admin':
        return "Unauthorized", 403
    
    course = get_course(id)

    result = delete_course_service(course)

    if result:
        flash("Course deleted Successfully")
    else:
        flash("Course deletion failed")

    return redirect(url_for('courses.list_course'))   

