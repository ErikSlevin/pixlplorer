# DB Setup
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class Step1Form(FlaskForm):
    db_host = StringField('DB Host', validators=[DataRequired()], default=os.environ.get("DB_HOST", "localhost"))
    db_user = StringField('DB User', validators=[DataRequired()], default=os.environ.get("DB_USER", "root"))
    db_password = PasswordField('DB Password', default=os.environ.get("DB_PASSWORD", ""))
    db_name = StringField('DB Name', validators=[DataRequired()], default=os.environ.get("DB_NAME", ""))
    submit = SubmitField('Weiter')

class Step2Form(FlaskForm):
    submit = SubmitField('Weiter')
