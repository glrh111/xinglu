from flask import jsonify, make_response
from . import api
from ..exceptions import ValidationError

def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

# now that this handler could catch this error through all routes
@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])