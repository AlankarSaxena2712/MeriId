from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import exception_handler


def success_response(payload, status=HTTP_200_OK):
    return Response({'data': payload}, status=status)


def create_response(payload):
    return success_response(payload, HTTP_201_CREATED)


def empty_response():
    return success_response({}, HTTP_204_NO_CONTENT)


def error_response(payload, status):
    return Response({'data': None, 'errors': payload}, status=status)


def bad_request_response(payload):
    return error_response(payload, HTTP_400_BAD_REQUEST)


def unauthorized_response(payload):
    return error_response(payload, HTTP_401_UNAUTHORIZED)


def forbidden_response(payload):
    return error_response(payload, HTTP_403_FORBIDDEN)


def not_found_response(payload):
    return error_response(payload, HTTP_404_NOT_FOUND)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        return error_response(response.data, response.status_code)

    return response
