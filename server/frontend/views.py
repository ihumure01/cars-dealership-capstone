from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Welcome to Best Cars Dealership",
        "status": "Application is running"
    })
