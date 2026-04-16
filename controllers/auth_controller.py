from flask import Blueprint, request, render_template, url_for, redirect, session
from services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods = {"GET", "POST"} )
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        role = "student"
        

        user = register_user(username, password, role)

        if user:
            session['username'] = user.username
            session['role'] = user.role
            session['user_id'] = user.id
            return redirect(url_for('main.dashboard'))  
        else:
            return render_template("index.html", error = "User already exits")
    else:
        return render_template('register.html')

@auth_bp.route("/login", methods= ["GET", "POST"])
def login():
   if request.method == "POST":
      username = request.form.get('username')
      password = request.form.get('password')

      user = login_user(username, password)

      if user:
           session['username'] = username
           session['role'] = user.role
           session['user_id'] = user.id
           return redirect(url_for('main.dashboard'))
      else:
           return render_template('index.html', error = "sth wrong")
   else:
       return render_template('login.html')

@auth_bp.route("/logout", methods=["GET"])  
def logout():
    session.clear()
    return redirect(url_for('main.home')) 
