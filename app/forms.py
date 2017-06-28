from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    jobname = StringField(u'jobname', validators=[DataRequired()])
    clientname = SelectField(u'clientname', validators=[DataRequired()])
    accountmanager = StringField(u'accountmanager', validators=[DataRequired()])
    submit = SubmitField(u'Submit')
