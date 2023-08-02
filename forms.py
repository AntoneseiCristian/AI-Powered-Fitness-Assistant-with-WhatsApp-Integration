from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    activity_level = SelectField('Activity Level', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    phone_number = StringField('Phone Number')
    account_sid = StringField('Account SID')
    auth_token = StringField('Auth Token')
    submit = SubmitField('Save')
