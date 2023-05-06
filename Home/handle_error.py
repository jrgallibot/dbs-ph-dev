from django.http import HttpResponse

class Handle524ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 524:
            # Handle the 524 error here
            return HttpResponse("524 Error: Server timeout error. Please try again later.")
        return response
