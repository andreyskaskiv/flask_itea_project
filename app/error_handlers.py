from flask import render_template, request, jsonify


def internal_server_error(error):
    if request.path.startswith('/api'):
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template(
        'error.html',
        title='Error 500',
        error=error
    ), 500


def page_not_found(error):
    if request.path.startswith('/api'):
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template(
        'error.html',
        title='Error 404',
        error=error
    ), 404


def forbidden(error):
    if request.path.startswith('/api'):
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template(
        'error.html',
        title='Error 403',
        error=error
    ), 403
