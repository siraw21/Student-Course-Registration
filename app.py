from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

# Create Flask Instance
app = Flask(__name__)

# Connection String
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/course_registration_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'first_secret_key'

# Create SQLALchemy instance
db = SQLAlchemy(app)

# Create instance of migration
migrate = Migrate(app, db)

# Create Models
class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(100), nullable=False)
     role = db.Column(db.String(100), nullable=False, default="student")
     password_hash = db.Column(db.String(255), nullable=False)

     created_At = db.Column(db.DateTime, server_default=func.now())

     def set_password(self, password):
        self.password_hash = generate_password_hash(password)
     
     def check_password(self, password):
        return check_password_hash(self.password_hash, password)

     def __repr__(self):
       return f"Name : {self.name}, Role: {self.role}"

class Course(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(50), nullable=False)
     code = db.Column(db.String(20), nullable=False)

     created_At = db.Column(db.DateTime, server_default=func.now())

     def to_dict(self):
        return {
           "id": self.id,
           "title": self.title,
           "code": self.code
        }

     def __repr__(self):
       return f"Title : {self.title}, Code: {self.code}" 

class Enrollment(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
     student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

     created_At = db.Column(db.DateTime, server_default=func.now())

     course = db.relationship('Course', backref='enrollments')
     student = db.relationship('User', backref='enrollments')
   

     def __repr__(self):
       return f"Course : {self.course_id}, Student: {self.student_id}"


# Create Routes

@app.route("/")
def home():
  return render_template('index.html')



# Auth routes
@app.route("/login", methods=["GET","POST"])
def login():
   if request.method == "GET":
       return render_template('login.html')
   elif request.method == "POST":
      username = request.form.get('username')
      password = request.form.get('password')

      user = User.query.filter_by(username = username).first()

      if user and user.check_password(password):
            session['username'] = username
            session['role'] = user.role
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
      else: 
         return render_template('index.html', error = "sth wrong")

@app.route("/register", methods=["GET","POST"])
def register():
   if request.method == "GET":
      return render_template('register.html')
   elif request.method == "POST":
      username = request.form.get('username')
      password = request.form.get('password')
      role = "student"
      
      user = User.query.filter_by(username = username).first()
      if user and user.check_password(password):
            return render_template("index.html", error = "User already exits")
      else:
          
          new_user = User(username = username)
          new_user.set_password(password)

          db.session.add(new_user)
          db.session.commit()
          user = User.query.filter_by(username = username).first()
          session['username'] = username
          session['role'] = role
          session['user_id'] = user.id
          return redirect(url_for('dashboard'))
      
@app.route("/create_admin")
def create_admin():
    new_user = User(username = "admin", role = "admin")
    new_user.set_password("admin123")

    db.session.add(new_user)
    db.session.commit()
    session['username'] = "admin"
    session['role'] = "admin"
    return redirect(url_for('dashboard'))
      
@app.route("/dashboard")
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
        
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/new_course", methods=['GET','POST'])
def create_course():
   if 'user_id' not in session:
        return redirect(url_for('login'))
   else:
      if request.method == 'POST':
         title = request.form.get('title')
         code = request.form.get('code')

         # Course logic
         if title and code :
            course = Course(title = title, code = code)

            db.session.add(course)
            db.session.commit()
            return redirect(url_for('dashboard'))
      else:
         return render_template('create_course.html')


@app.route("/courses")
def list_course():
   if 'user_id' not in session:
        return redirect(url_for('login'))
   courses = Course.query.all()
   result = [course.to_dict() for course in courses]
         
   return render_template('list_course.html', result=result)

@app.route("/enrollment", methods=["GET", "POST"])
def enroll_course():
      if 'user_id' not in session:
        return redirect(url_for('login'))
      
      if request.method == "GET":
         courses = Course.query.all()
         result = [course.to_dict() for course in courses]
         return render_template('enroll_course.html', result=result)
      elif request.method == "POST":
         course_id = request.form.get('course_id')
         student_id = session.get('user_id');

         enrollment = Enrollment(course_id = course_id, student_id = student_id)
         db.session.add(enrollment)
         db.session.commit()
         return redirect(url_for('dashboard'))
      else:
         return "Error at enroll course"


@app.route("/list_enrollments",)
def list_enrolled_students():
      if 'user_id' not in session:
        return redirect(url_for('login'))
      enrollments = Enrollment.query.all()
         
      return render_template('list_enrollments.html', result=enrollments)

# Run app
if __name__ == "__main__":
    app.run(debug=True)