from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User
from wtforms.fields.html5 import DateField, TimeField

class IndexForm(FlaskForm):
    title = TextAreaField('New Task', validators = [DataRequired()])
    submit = SubmitField(label = 'Create Task')

class AssignmentButton(FlaskForm):
    submit = SubmitField(label = 'New Assignment')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AssignmentForm(FlaskForm):
    title = StringField('Assignment Name', validators = [DataRequired()])
    class_name = StringField('Class Name', validators = [DataRequired()])
    summary = TextAreaField('Summary...')
    due_date = DateField('Due Date', format='%Y-%m-%d')
    due_time = TimeField('Due Time')
    submit = SubmitField('Create Assignment')
