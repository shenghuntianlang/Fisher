"""
the request parameter verification for book
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class Searchform(Form):
    """
    继承自flask的Form类,对浏览器传入参数进行验证
    """
    q = StringField(validators=[Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class DriftForm(Form):
    recipient_name = StringField(validators=[DataRequired(),
                                             Length(min=2, max=20, message='收件人姓名长度必须在2到20个字符之间')])

    mobile = StringField(validators=[DataRequired(), Regexp('^1[0-9]{10}$', 0, message='请输入正确的手机号')])

    message = StringField()

    address = StringField(validators=[DataRequired(), Length(min=10, max=70, message='地址过于简单,请尽量详细些')])
