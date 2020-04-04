from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField, validators


# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')

# class UserCustomForm(FlaskForm):
#     first_name = StringField('First name', validators=[
#         validators.DataRequired('First name is required')])
#     last_name = StringField('Last name', validators=[
#         validators.DataRequired('Last name is required')])
#     email = StringField('Email', validators=[
#         validators.DataRequired('Email is required')])
#     password = StringField('Password')
#     roles = SelectMultipleField(label='Roles', coerce=int)
#     submit = SubmitField('Save')

# class RoleCustomForm(FlaskForm):
#     name = StringField('Role name', validators=[
#         validators.DataRequired('Role name is required')])
#     label = StringField('Role label')
#     submit = SubmitField('Save')