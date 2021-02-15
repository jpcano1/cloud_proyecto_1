def response_with(response, value=None,
                  error=None, headers={},
                  pagination=None):
    """
    Function to send responses throughout the application
    :param response: The response code and message
    :param value: The value to be sent in the response body
    :param error: The error produced by the logic in the views
    :param headers: The headers of the response
    :param pagination: The pagination index
    :return: The response of the performed request of the user
    """
    result = {}
    if value:
        result.update(value)

    if response.get("message", None):
        result.update({
            "message": response["message"]
        })

    result.update({
        "code": response["code"]
    })

    if error:
        result.update({
            "errors": error
        })

    if pagination:
        result.update({
            "pagination": pagination
        })

    headers.update({
        "Access-Control-Allow-Origin": "*"
    })
    headers.update({
        "server": "Flask REST API"
    })

    return result, response["status"], headers

# Responses
INVALID_FIELD_NAME_SENT_422 = {
    "status": 422,
    "code": "invalidField",
    "message": "Invalid fields found"
}

INVALID_INPUT_422 = {
    "status": 422,
    "code": "invalidInput",
    "message": "Invalid input"
}

MISSING_PARAMETERS_422 = {
    "status": 422,
    "code": "missingParameter",
    "message": "Missing parameters."
}

BAD_REQUEST_400 = {
    "status": 400,
    "code": "badRequest",
    "message": "Bad request"
}

SERVER_ERROR_500 = {
    "status": 500,
    "code": "serverError",
    "message": "Server error"
}

SERVER_ERROR_404 = {
    "status": 404,
    "code": "notFound",
    "message": "Resource not found"
}

FORBIDDEN_403 = {
    "status": 403,
    "code": "notAuthorized",
    "message": "You are not authorised to execute this."
}
UNAUTHORIZED_401 = {
    "status": 401,
    "code": "notAuthorized",
    "message": "Invalid authentication."
}

NOT_FOUND_HANDLER_404 = {
    "status": 404,
    "code": "notFound",
    "message": "route not found"
}

SUCCESS_200 = {
    'status': 200,
    'code': 'success',
}

SUCCESS_201 = {
    'status': 201,
    'code': 'success'
}

SUCCESS_204 = {
    'status': 204,
    'code': 'success'
}