from django.conf import settings
from django.contrib.messages.storage import default_storage
from django.utils.deprecation import MiddlewareMixin


class RequestManipulateMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._messages = default_storage(request)