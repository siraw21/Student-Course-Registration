from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
     full_name = StringField("Full Name:", validators=[DataRequired()])
     student_id = StringField("Student Id:", validators=[DataRequired(), Length(min=6, message = 'Minimum Length 6 Characters'), ])
     email = StringField("Email", validators=[DataRequired(), Email()])
     year = SelectField("Year", choices=[
          ("2", "Second Year"),
          ("3", "Third Year"),
          ("4", "Fourth Year"),
          ("5", "Fifth Year"),
     ], validators=[DataRequired()])
     password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=12)])
     confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message ='Passwords must match')])
     submit = SubmitField('Register')

class LoginForm(FlaskForm):
    full_name = StringField('User Name:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired() ]) 

    submit = SubmitField('Login')     


class EditProfileForm(FlaskForm):
     full_name = StringField("Full Name:", validators=[DataRequired()])
     student_id = StringField("Student Id:", validators=[DataRequired(), Length(min=6, message = 'Minimum Length 6 Characters'), ])
     email = StringField("Email", validators=[DataRequired(), Email()])
     year = SelectField("Year", choices=[
          ("2", "Second Year"),
          ("3", "Third Year"),
          ("4", "Fourth Year"),
          ("5", "Fifth Year"),
     ], validators=[DataRequired()])    
     submit = SubmitField('Save Change')