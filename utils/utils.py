from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status


def error_response(message: str, key=None | str):
    if key:
        dict_response = {key: _(message)}
    else:
        dict_response = {"error": _(message)}
    return Response(dict_response, status=status.HTTP_400_BAD_REQUEST)
