from flask import Flask
from config import Config
from extensions import db, migrate

# Models for migration
from models import User, Course, Enrollment, Student_Profile

#  import controllers or blueprints
from controllers.main_controller import main_bp
from controllers.auth_controller import auth_bp
from controllers.course_controller import course_bp
from controllers.enrollment_controller import enrollment_bp
from controllers.student_controller import student_bp


def create_app():
   app = Flask(__name__)
   app.config.from_object(Config)

   db.init_app(app)
   migrate.init_app(app, db)

   # register blueprints
   app.register_blueprint(main_bp)
   app.register_blueprint(auth_bp)
   app.register_blueprint(course_bp)
   app.register_blueprint(enrollment_bp)
   app.register_blueprint(student_bp)
   
   return app


# Run app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)