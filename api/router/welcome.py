from flask import Blueprint

home_api = Blueprint('home', __name__)


@home_api.route('/')
def welcome():
    return "Welcome to flask api!"
