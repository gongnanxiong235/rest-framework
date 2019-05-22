from rest_framework.exceptions import APIException
class BlackException(APIException):
    status_code = 401
    default_detail = 'black user.'
    default_code = 'authentication_failed'


class AuthenticationFailed(APIException):
    status_code = 401
    default_detail = 'token check failed.'
    default_code = 'authentication_failed'

class RegistException(APIException):
    status_code = 401
    default_detail = 'black user.'
    default_code = 'authentication_failed'