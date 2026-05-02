from django.http import HttpResponse
from django.conf import settings


class SimpleCorsMiddleware:
    allowed_origins = set(getattr(settings, 'FRONTEND_ORIGINS', [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
    ]))

    allowed_methods = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    allowed_headers = 'Authorization, Content-Type, Accept, Origin, X-Requested-With'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'OPTIONS':
            response = HttpResponse(status=204)
            self.add_cors_headers(request, response)
            return response

        response = self.get_response(request)
        self.add_cors_headers(request, response)
        return response

    def add_cors_headers(self, request, response):
        origin = request.headers.get('Origin')

        if origin in self.allowed_origins:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Methods'] = self.allowed_methods
            response['Access-Control-Allow-Headers'] = self.allowed_headers
            response['Vary'] = 'Origin'