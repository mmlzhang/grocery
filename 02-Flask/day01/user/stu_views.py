from flask import render_template, Blueprint


stu_blue_print = Blueprint('stu', __name__)


@stu_blue_print.route('/')
def scores():

    return '分数'
