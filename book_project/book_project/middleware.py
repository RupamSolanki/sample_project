import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from common.constant import constants


class BadRequestMiddleware(object):
    """
    This middleware class is used to handle the bad request.

    :param object:
    :type object: object
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.__class__ == HttpResponseNotFound:
            if "rest" in request.path:
                data = {constants["Error"]: constants["URLNotFound"].format(request.path)}
                response = HttpResponse(
                    json.dumps(data), content_type="application/json", status=404
                )
            else:
                return render(template_name="error.html", request=request)
        return response