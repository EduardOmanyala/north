from django.utils.deprecation import MiddlewareMixin
from .models import RequestCount

class TrackGetRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "GET":
            RequestCount.increment()