from flask import jsonify

from app.exceptions import ValidationError
from app.api import api


def bad_request(message):
    """ Non-existent request """
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    """ Not authorized user """
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    """ Only admin rights """
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(ValidationError)
def validation_error(error):
    return bad_request(error.args[0])
