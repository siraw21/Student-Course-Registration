from flask import Blueprint, render_template, session

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
  return render_template('index.html')

@main_bp.route("/dashboard")
def dashboard():
    if "user_id" in session:
         if session['role'] == "student":
            return render_template('student_dashboard.html')
         elif session['role'] == "admin":
            return render_template('admin_dashboard.html')
         else:
            return render_template('index.html', error= "Invalid role")
    else:
        return render_template('index.html', error= "doesn't access")