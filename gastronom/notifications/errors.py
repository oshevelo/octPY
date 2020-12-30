from rest_framework.exceptions import APIException
from rest_framework import status


class CustomForbidden(APIException):
    status_code = status.HTTP_404_NOT_FOUND
