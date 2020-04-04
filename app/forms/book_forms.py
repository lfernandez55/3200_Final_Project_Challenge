# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators




# Define the User profile form
class BookForm(FlaskForm):
    author = StringField('Author', validators=[
        validators.DataRequired('This is a required field')])
    title = StringField('Last name', validators=[
        validators.DataRequired('This is a required field')])
    submit = SubmitField('Save')