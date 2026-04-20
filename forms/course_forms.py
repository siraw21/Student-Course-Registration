from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class CourseDetailForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    code = StringField("Course Code:", validators=[DataRequired()])
    credit_hours = IntegerField("Credit Hours:", validators=[DataRequired()])
    description = StringField("Description:", validators=[DataRequired()])
    category = SelectField("Category:", choices= [ 
        ('Major Course', 'Major Course'),
        ('Supporting Course', 'Supporting Course'),
        ('Common Course', 'Common Course'),
    ], validators=[DataRequired()])
    instructor_name = StringField('Instructor Name:', validators=[DataRequired()])
    required_year = IntegerField("Required_year:", validators=[DataRequired()])
    submit = SubmitField('Add')

   