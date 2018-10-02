from flask import render_template, request, Blueprint


blue = Blueprint('first', __name__)


@blue.route('/hello/')
def hello():
    return render_template('hello.html')


@blue.route('/hello/<name>/', methods=['POST', "GET"])
def hello_name(name):
    if request.method == 'GET':
        return render_template('hello.html', name=name)


@blue.route('/hello/<float:float>/')
def float(float):
    return render_template('hello.html', float=float)


@blue.route('/hello/<int:int>/')
def float1(int):
    return render_template('hello.html', int=int)


@blue.route('/hello/<path:path>/')
def show(path):
    return render_template('hello.html', path=path)


@blue.route('/hello/<uuid:uuid>/')
def uuid1(uuid):
    return render_template('hello.html', uuid=uuid)

