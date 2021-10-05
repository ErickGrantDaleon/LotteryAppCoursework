from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, ValidationError, Length

# TODO: Password must be between 6 and 12 characters in length.
# TODO: Password must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 special character.
# TODO: Password and Confirm Password must match.
# TODO: PIN Key must be exactly 32 characters in length.
# TODO: Relevant validation error messages must be shown.

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
    password = PasswordField(validators=[Required()])
    confirm_password = PasswordField(validators=[Required()])
    pin_key = StringField(validators=[Required()])
    submit = SubmitField()
