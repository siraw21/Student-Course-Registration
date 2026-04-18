from flask import  Blueprint, render_template, redirect, request, session, url_for, jsonify
from models import User
from services.enrollment_service import enroll_course, list_enrollment_courses, list_enrolled_courses


enrollment_bp = Blueprint("enrollments", __name__)

@enrollment_bp.route("/enrollment", methods=["GET", "POST"])
def enroll():
      if 'user_id' not in session:
        return redirect(url_for('auth.login'))
      
      if request.method ==  "GET":
         courses = list_enrollment_courses()
         result = [course.to_dict() for course in courses]  
         return render_template('enroll_course.html', result=result)
      elif request.method == "POST":
         data = request.get_json()
         # course_id = request.form.get('course_id')
         course_id = data.get("course_id")
         student_id = session.get('user_id');

         enrolled = enroll_course(course_id, student_id)

         if enrolled:
            # return redirect(url_for('main.dashboard'))
            return jsonify({'success': True})
         else:
             return jsonify({'success': False})
      else:
         return "Error at enroll course"
      
@enrollment_bp.route("/list_enrollments",)
def enrolled_courses():
      if 'user_id' not in session:
        return redirect(url_for('auth.login'))
      user_id = session.get('user_id')
      user = User.query.get(user_id)
      enrollments = list_enrolled_courses(user) 
         
      return render_template('list_enrollments.html', enrollments=enrollments)      