from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, ValidationError, Length, EqualTo
import re

def character_check(form,field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed.")

def phone_check(form,field):
    if len(field.data) != 13:
        raise ValidationError("Phone must be of the form XXXX-XXX-XXXX.")
    for i, char in enumerate(field.data):
        if not ((i in {4, 8} and char == "-") or char.isnumeric()):
            raise ValidationError("Phone must be of the form XXXX-XXX-XXXX.")

class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    phone = StringField(validators=[Required(), phone_check])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be between 6 and '
                                                                                   '12 characters long.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields '
                                                                                         'must be equal.')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='Pin key must be 32 characters '
                                                                                 'long.')])
    submit = SubmitField()

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9\s])')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 "
                                  "special character.")
