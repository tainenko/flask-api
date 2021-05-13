from flask import Blueprint

home_api = Blueprint('welcome', __name__)


@home_api.route('/')
def welcome():
    return "Hello World!"
