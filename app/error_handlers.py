from flask import render_template


def internal_server_error(error):
    return render_template(
        'error.html',
        title='Error 500',
        error=error
    ), 500


def page_not_found(error):
    return render_template(
        'error.html',
        title='Error 404',
        error=error
    ), 404
