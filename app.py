from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func

# Create Flask Instance
app = Flask(__name__)

# Connection String
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/course_registration_db'

# Create SQLALchemy instance
db = SQLAlchemy(app)

# Create instance of migration
migrate = Migrate(app, db)

# Create Models
class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), nullable=False)
     role = db.Column(db.String(100), nullable=False)

     createdAt = db.Column(db.DateTime, server_default=func.now())

     def __repr__(self):
       return f"Name : {self.name}, Role: {self.role}"

class Course(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(50), nullable=False)
     code = db.Column(db.String(20), nullable=False)

     createdAt = db.Column(db.DateTime, server_default=func.now())

     def __repr__(self):
       return f"Title : {self.title}, Code: {self.code}" 

class Enrollment(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
     student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

     createdAt = db.Column(db.DateTime, server_default=func.now())

     def __repr__(self):
       return f"Course : {self.course_id}, Student: {self.student_id}"


# Create Routes

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/student")
def student():
   return render_template('student_dashboard.html')

@app.route("/admin")
def admin():
   return render_template('admin_dashboard.html')

@app.route("/add_course", methods=['GET','POST'])
def add_course():

   if request.method == 'POST':
      title = request.form.get('title')
      code = request.form.get('code')

      # Course logic
      if title and code :
         course = Course(title = title, code = code)

         db.session.add(course)
         db.session.commit()
         return redirect(url_for('add_course'))
   else:
      return render_template('add_course.html')


@app.route("/courses")
def get_course():
   courses = Course.query.all()

   result = []
   if courses:
      for course in courses:
         result.append({
            'id': course.id,
            'title': course.title,
            'code': course.code
         })
         
   return render_template('get_course.html', result=result)

@app.route("/enrollment",)
def enroll_course():
      courses = Course.query.all()

      result = []
      if courses:
         for course in courses:
            result.append({
               'id': course.id,
               'title': course.title,
               'code': course.code
            })
         
      return render_template('enrollment.html', result=result)

@app.route("/enroll", methods=["GET"])
def enroll():
   
   course_id = request.args.get('course_id')
   student_id = 1;

   enrollment = Enrollment(course_id = course_id, student_id = student_id)
   db.session.add(enrollment)
   db.session.commit()

   return redirect(url_for('student'))

@app.route("/get_enrolled",)
def get_enrolled():
      enrollments = Enrollment.query.all()

      result = []
      if enrollments:
         for enrollment in enrollments:
            result.append({
               'id': enrollment.id,
               'course_id': enrollment.course_id,
               'student_id': enrollment.student_id
            })
         
      return render_template('get_enrolled.html', result=result)

# Run app
if __name__ == "__main__":
   #  with app.app_context():
   #    db.create_all()
    app.run(debug=True)