from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField, validators, PasswordField, FieldList, FormField, IntegerField, HiddenField
from wtforms_components import TimeField

class TimeCustomForm(FlaskForm):
    id = HiddenField(label="")
    time_day = SelectField(label="Day of Week",choices=[(1,'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday')], coerce=int)
    time_start = TimeField(label='Time Start') #see: https://stackoverflow.com/questions/44020690/wtforms-equivalent-to-input-type-time
    time_end = TimeField(label='Time End')
    
    class Meta:
        # No need for csrf token in this child form
        csrf = False


class UserCustomForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    email = StringField('Email', validators=[
        validators.DataRequired('Email is required')])
    password = PasswordField('Password')
    roles = SelectMultipleField(label='Roles', coerce=int)

    # tutor = FormField(TutorCustomForm, 'Tutor Specific Fields')
    # add_child = SubmitField(label='Tutor Specific Info')

    submit = SubmitField('Save')

class RoleCustomForm(FlaskForm):
    name = StringField('Role name', validators=[
        validators.DataRequired('Role name is required')])
    # label = StringField('Role label')
    submit = SubmitField('Save')

    # class Meta:
    #     # No need for csrf token in this child form
    #     csrf = False

class TutorCustomForm(UserCustomForm):
    phone = StringField(label='Phonex')
    remove_time_id = HiddenField(label="")
    dates = FieldList(FormField(TimeCustomForm), label='dates')
    add_time = SubmitField(label='Add Date')
    remove_time = SubmitField(label='Remove Date')
    