from flask import Blueprint


aj_blueprint = Blueprint('aj', __name__)

@aj_blueprint.route('/')
def index():
    return 'hello '