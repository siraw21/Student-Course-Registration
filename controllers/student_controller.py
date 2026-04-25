from flask import Blueprint,request, session, redirect, url_for, flash, render_template
from services.student_service import get_student_profile, populate_student_obj 
from forms.auth_forms import  EditProfileForm
from services.auth_service import get_current_user
from extensions import db

student_bp = Blueprint("students", __name__)


@student_bp.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
   
   if not session.get('user_id'):
      return redirect(url_for('auth.login'))
   
   user = get_current_user(session.get('user_id'))
   form = EditProfileForm()
   profile = user.student_profile

   if request.method == 'GET':
      form.full_name.data = user.full_name
      form.email.data = user.email
      form.student_id.data = profile.student_id
      form.year.data = profile.year
     

   if form.validate_on_submit():
      user.full_name = form.full_name.data
      user.email = form.email.data
      user.student_profile.student_id = form.student_id.data
      user.student_profile.year = form.year.data

      # print("test")
      session['username'] = user.full_name
      session['role'] = user.role
      session['user_id'] = user.id

      db.session.commit()
      flash("Profile updated successfully!", "success")
      return redirect(url_for('main.dashboard'))
        
   return render_template('edit_profile.html', form=form)

       

