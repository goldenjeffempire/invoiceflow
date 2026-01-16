import logging
import traceback
from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled Exception: {str(e)}")
            logger.error(traceback.format_exc())
            
            if settings.DEBUG:
                raise e
            
            return render(request, 'errors/500.html', status=500)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request: {request.method} {request.path} User: {request.user}")
        response = self.get_response(request)
        logger.info(f"Response: {response.status_code}")
        return response
