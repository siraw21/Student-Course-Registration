
class Config:
  SECRET_KEY = 'first_secret_key'
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/course_registration_db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False