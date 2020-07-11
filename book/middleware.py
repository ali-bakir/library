from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin


class RequestManipulateMiddleware(MiddlewareMixin):
    def process_request(self, request):
        data = request.POST

        if data.get('_method') and data.get('_method') == 'DELETE':
            request.method = 'DELETE'
            get_token(request)
