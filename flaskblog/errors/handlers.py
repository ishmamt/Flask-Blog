from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404  # have to return 2 things. For regular ones the code was 200. Didn't need to do it then

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403  # have to return 2 things. For regular ones the code was 200. Didn't need to do it then

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500  # have to return 2 things. For regular ones the code was 200. Didn't need to do it then
