"""
The request parameter verification for auth
"""
from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(message='邮箱不能为空,请输入您的邮箱'),
                                    Length(8, 64), Email(message='电子邮箱不符合规范')])

    nickname = StringField(validators=[DataRequired(message='用户名不能为空,请输入您的用户名'),
                                       Length(2, 10, message='昵称至少需要两个字符,最多10个字符')])

    password = PasswordField(validators=[DataRequired(message='密码不可以为空,请输入你的密码'), Length(6, 32)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该电子邮件已被注册!')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('该昵称已存在!')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(message='邮箱不能为空,请输入您的邮箱'),
                                    Length(8, 64), Email(message='电子邮箱不符合规范')])

    password = PasswordField(validators=[DataRequired(message='密码不可以为空,请输入你的密码'), Length(6, 32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(message='邮箱不能为空,请输入您的邮箱'),
                                    Length(8, 64, message='电子邮箱长度必须在8到64个字符之间'),
                                    Email(message='电子邮箱不符合规范')])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(message='邮箱不能为空,请输入您的邮箱'),
        Length(6, 32, message='密码长度必须在6到32个字符之间'),
        EqualTo('password2', message='两次输入的密码不符')
    ])
    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32)
    ])
