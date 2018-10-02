from flask_wtf import Form
import wtforms as wtf
from wtforms import validators as vld


class LoginForm(Form):
    email = wtf.StringField('Email', validators=[vld.Required(),
                                                 vld.Length(1, 64),
                                                 vld.Email()
                                                 ])
    password = wtf.PasswordField('Password', validators=[vld.Required()])
    remember_me = wtf.BooleanField('Keep me logged in')
    submit = wtf.SubmitField('Log In')