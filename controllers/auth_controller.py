from flask import Blueprint, flash, request, render_template, url_for, redirect, session
from services.auth_service import register_user, login_user
from services.student_service import create_student_profile
from forms.auth_forms import RegisterForm, LoginForm


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods = {"GET", "POST"} )
def register():
        form = RegisterForm()

        if form.validate_on_submit():
            full_name = form.full_name.data
            student_id = form.student_id.data
            email = form.email.data
            year = form.year.data
            password = form.password.data
            # confirm = form.confirm.data
            role = "student"


            user = register_user(full_name, email, password, role)

            if user:
                session['username'] = user.full_name
                session['role'] = user.role
                session['user_id'] = user.id
                student_profile = create_student_profile(user.id, student_id, year)
                if student_profile:
                    return redirect(url_for('main.dashboard'))  
            else:
                flash('User Already exits')
                return redirect(url_for('auth.register'))
        else:
            return render_template('register.html', form = form)

@auth_bp.route("/login", methods= ["GET", "POST"])
def login():
      form = LoginForm()

      if form.validate_on_submit():
        full_name = form.full_name.data
        password = form.password.data

        user = login_user(full_name, password)

        if user:
            session['username'] = user.full_name
            session['role'] = user.role
            session['user_id'] = user.id
            flash(f"Welcome back, {session['username']}!")
            return redirect(url_for('main.dashboard'))
        else:
            flash('Password or Username invalid')
            return redirect(url_for('auth.login'))
      else:
         return render_template('login.html', form = form)

@auth_bp.route("/logout", methods=["GET"])  
def logout():
    session.clear()
    return redirect(url_for('main.home')) 


