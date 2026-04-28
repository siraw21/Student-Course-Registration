from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
  return render_template('index.html')

@main_bp.route("/dashboard")
def dashboard():
    if "user_id" in session:
         if session['role'] == "student":
            return redirect(url_for('enrollments.enroll'))
         elif session['role'] == "admin":
            return render_template('admin_dashboard.html')
         else:
            return render_template('index.html', error= "Invalid role")
    else:
        return render_template('index.html', error= "doesn't access")
    



