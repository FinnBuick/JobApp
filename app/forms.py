from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SelectField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import DateField
from wtforms import BooleanField
from wtforms.validators import *


class RegistrationForm(FlaskForm):
    username     = StringField('Username', validators=[length(min=4, max=25)])
    email        = StringField('Email Address', validators=[length(min=6, max=35)])
    password = PasswordField('Enter Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    register = SubmitField(u'Register')

class JobForm(FlaskForm):
    jobname = StringField(u'jobname', validators=[DataRequired(), length(max=65)])
    clientname = SelectField(u'clientname', validators=[DataRequired(), length(max=65)])
    installdate = DateField(u'installdate',format='%Y-%m-%d',  validators=[DataRequired()])
    accountmanager = SelectField(u'accountmanager', validators=[DataRequired(), length(max=65)])
    submit = SubmitField(u'Submit')
