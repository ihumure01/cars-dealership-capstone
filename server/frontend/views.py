from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return JsonResponse({
        "message": "Welcome to Best Cars Dealership",
        "status": "Application is running"
    })

@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "message": "Login successful",
                "username": user.username
            })

        return JsonResponse({"error": "Invalid username or password"}, status=401)

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

@csrf_exempt
def logout_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    logout(request)
    return JsonResponse({"message": "Logout successful"})
