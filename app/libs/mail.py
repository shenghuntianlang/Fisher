"""
custom tools for mails
"""
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_mail(app, msg):
    """
    异步发送邮件,避免页面停顿
    :param app:
    :param msg:
    :return:
    """
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as ex:
            raise ex


def send_mail(to, subject, template, **kwargs):
    # msg = Message('测试邮件', sender='1741824619@qq.com', body='Test', recipients=['1741824619@qq.com'])
    msg = Message('[鱼书] ' + subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 获取current_app中的app对象
    # 如果仅传入current_app,会由于线程隔离导致异步发送时找不到app上下文
    app = current_app._get_current_object()
    # 如果在使用新线程时传入参数,只需要传入args关键词参数即可
    new_thread = Thread(target=send_async_mail, args=[app, msg])
    new_thread.start()
