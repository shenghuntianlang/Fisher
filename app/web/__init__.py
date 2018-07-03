"""
register for web blueprint
"""
from flask import Blueprint, render_template, request, current_app

web = Blueprint('web', __name__)


# 全局监听异常码,并自动执行以下代码
@web.app_errorhandler(404)
def not_found(ex):
    error = []
    return render_template('404.html', error=error), 404


from . import book, auth, drift, gift, main, wish
