"""
Flask-WTF form definitions for Campus IoT Management.
"""

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField,
    SubmitField, HiddenField, TextAreaField, SelectField
)
from wtforms.validators import DataRequired, Length, Optional

class LoginForm(FlaskForm):
    """Used on /login to authenticate both admins and students."""
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=64)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=128)]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SensorForm(FlaskForm):
    """Adds or edits an IoT sensor (admin only)."""
    name = StringField(
        'Sensor Name',
        validators=[DataRequired(), Length(max=64)]
    )
    location = StringField(
        'Location',
        validators=[DataRequired(), Length(max=128)]
    )
    status = SelectField(
        'Status',
        choices=[('online','Online'), ('offline','Offline')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Save Sensor')


class CalibrationForm(FlaskForm):
    """Records a calibration event for a sensor (admin only)."""
    sensor_id = HiddenField(validators=[DataRequired()])
    notes = TextAreaField(
        'Calibration Notes',
        validators=[Optional(), Length(max=512)]
    )
    submit = SubmitField('Calibrate')


class FeedbackForm(FlaskForm):
    """Student temperature feedback form."""
    sensor_id = SelectField(
        'Select Room/Sensor',
        coerce=int,
        validators=[DataRequired()]
    )
    rating = SelectField(
        'Temperature Feeling',
        choices=[('hot','Hot'), ('ok','OK'), ('cold','Cold')],
        validators=[DataRequired()]
    )
    comment = TextAreaField(
        'Additional Comments',
        validators=[Optional(), Length(max=512)]
    )
    submit = SubmitField('Submit Feedback')


class ActionForm(FlaskForm):
    """
    Generic hidden-field form for actions like removing a sensor or calibrating.
    We’ll pass record IDs in the hidden field.
    """
    record_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Go')
