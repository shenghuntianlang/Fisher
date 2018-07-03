"""
the view functions about some operations for user authentication
"""

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.base import db
from app.models.user import User
from . import web

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)

            # 获取重定向路径并跳转,如果重定向路径不存在,
            # 则跳转到主页
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                return redirect(url_for('web.index'))
            return redirect(next)
            # 开启cookie持续保留
            # login_user(user, remember=True)
        else:
            flash('账户不存在或密码错误!')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            ## 如果user中未查询到数据,则抛出异常
            user = User.query.filter_by(email=account_email).first_or_404()
            from app.libs.mail import send_mail
            send_mail(form.email.data, '重置您的密码', 'email/reset_password.html', user=user,
                      token=user.generate_token())
            flash('电子邮件已发送,请到您的电子邮箱中查收')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        if User.reset_password(token, form.password1.data):
            flash('你的密码已更新,请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
