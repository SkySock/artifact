from rest_framework.exceptions import APIException


class PostNotModified(APIException):
    status_code = 403
    default_detail = 'Post status is published. Not modified'
    default_code = 'not_modified'
