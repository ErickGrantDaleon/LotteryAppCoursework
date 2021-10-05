from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

# TODO: Email must be a valid email address.
# TODO: Firstname and Lastname must not contain the following characters:  * ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >
# TODO: Phone must be of the form XXXX-XXX-XXXX
# TODO: Password must be between 6 and 12 characters in length.
# TODO: Password must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 special character.
# TODO: Password and Confirm Password must match.
# TODO: PIN Key must be exactly 32 characters in length.
# TODO: Relevant validation error messages must be shown.

class RegisterForm(FlaskForm):
    email = StringField(validators=[Required()])
    firstname = StringField(validators=[Required()])
    lastname = StringField(validators=[Required()])
    phone = StringField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    confirm_password = PasswordField(validators=[Required()])
    pin_key = StringField(validators=[Required()])
    submit = SubmitField()
