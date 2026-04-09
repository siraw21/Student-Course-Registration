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

     created_At = db.Column(db.DateTime, server_default=func.now())

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

@app.route("/student")
def student():
   return render_template('student_dashboard.html')

@app.route("/admin")
def admin():
   return render_template('admin_dashboard.html')

@app.route("/new_course", methods=['GET','POST'])
def create_course():

   if request.method == 'POST':
      title = request.form.get('title')
      code = request.form.get('code')

      # Course logic
      if title and code :
         course = Course(title = title, code = code)

         db.session.add(course)
         db.session.commit()
         return redirect(url_for('admin'))
   else:
      return render_template('create_course.html')


@app.route("/courses")
def list_course():
   courses = Course.query.all()
   result = [course.to_dict() for course in courses]
         
   return render_template('list_course.html', result=result)

@app.route("/enrollment", methods=["GET", "POST"])
def enroll_course():
      if request.method == "GET":
         courses = Course.query.all()
         result = [course.to_dict() for course in courses]
         return render_template('enroll_course.html', result=result)
      elif request.method == "POST":
         course_id = request.form.get('course_id')
         student_id = 1;

         enrollment = Enrollment(course_id = course_id, student_id = student_id)
         db.session.add(enrollment)
         db.session.commit()
         return redirect(url_for('student'))
      else:
         return "Error at enroll course"

# @app.route("/enroll", methods=["POST"])
# def enroll():
   
#    course_id = request.form.get('course_id')
#    student_id = 1;

#    enrollment = Enrollment(course_id = course_id, student_id = student_id)
#    db.session.add(enrollment)
#    db.session.commit()

#    return redirect(url_for('student'))

@app.route("/list_enrollments",)
def list_enrolled_students():
      enrollments = Enrollment.query.all()

      # result = []
      # if enrollments:
      #    for enrollment in enrollments:
      #       result.append({
      #          'id': enrollment.id,
      #          'course_id': enrollment.course_id,
      #          'student_id': enrollment.student_id,
      #          'createdAt': enrollment.created_At
      #       })
         
      return render_template('list_enrollments.html', result=enrollments)

# Run app
if __name__ == "__main__":
   #  with app.app_context():
   #    db.create_all()
    app.run(debug=True)