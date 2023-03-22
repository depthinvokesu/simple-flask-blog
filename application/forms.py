from wtforms import Form, StringField, PasswordField, EmailField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class CreatePostForm(Form):
    """Form for a new post"""
    title = StringField(
        'Title',
        validators=
        [
            InputRequired(),
            Length(min=5, message="Title should be at least 5 characters long")
        ]
    )
    body=TextAreaField(
        'Text',
        validators=
        [
            InputRequired()
        ]
    )
    # This field is for custom tag
    tag = StringField(
        'Tag',
        validators=
        [
            Length(max=10, message="Tag cannot be longer than 10 characters")
        ]
    )


class SignUpForm(Form):
    """Form for creating a new user"""
    email = EmailField(
        'E-mail',
        validators=
        [
            InputRequired(message="Please enter your email"),
            Email(message="Not a valid email address")

        ]
    )
    name = StringField(
        'Name',
        validators=
        [
            InputRequired(message="Please enter your name")
        ]
    )
    password = PasswordField(
        "Password",
        [
            InputRequired(message="Please enter a password"),
            Length(min=3, message="Password should be at least 3 characters long"),
            EqualTo('password_confirm', message="Passwords must match")
        ]
    )
    password_confirm = PasswordField(
        'Confirm Password'
    )
    submit = SubmitField(
        'Submit'
    )



class SignInForm(Form):
    """Form for sign-in page"""
    email = EmailField(
        'E-mail',
        validators=
        [
            InputRequired(message="Please enter your email"),
            Email(message="Not a valid email address")
        ]
    )
    password = PasswordField(
        'Password',
        [
            InputRequired(message="Please enter a password"),
            Length(min=3, message="Password should be at least 3 characters long")
        ]
    )
    submit = SubmitField(
        'Submit'
    )

