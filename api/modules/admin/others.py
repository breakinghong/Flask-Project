
from flask import render_template

from api.libs.redprint import Redprint

api = Redprint('index')


@api.route('/unicode')
def unicode():
    return render_template('X-admin/unicode.html')


@api.route('/error')
def error():
    return render_template('X-admin/error.html')


@api.route('/log')
def log():
    return render_template('X-admin/log.html')


@api.route('/demo')
def demo():
    return render_template('X-admin/demo.html')

