from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Dealer
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


def get_dealer_reviews(request, dealer_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    dealer = get_object_or_404(Dealer, id=dealer_id)
    reviews = dealer.reviews.all()

    data = [
        {
            "id": review.id,
            "reviewer_name": review.reviewer_name,
            "comment": review.comment,
            "rating": review.rating,
            "created_at": review.created_at.isoformat()
        }
        for review in reviews
    ]

    return JsonResponse({
        "dealer_id": dealer.id,
        "dealer_name": dealer.name,
        "reviews": data
    })


def get_all_dealers(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    dealers = Dealer.objects.all()

    data = [
        {
            "id": dealer.id,
            "name": dealer.name
        }
        for dealer in dealers
    ]

    return JsonResponse({"dealers": data})


def get_dealer_by_id(request, dealer_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    dealer = get_object_or_404(Dealer, id=dealer_id)

    return JsonResponse({
        "id": dealer.id,
        "name": dealer.name
    })


def get_dealers_by_state(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    dealers = Dealer.objects.filter(state__iexact="Kansas")

    data = [
        {"id": dealer.id, "name": dealer.name, "state": dealer.state}
        for dealer in dealers
    ]

    return JsonResponse({"dealers": data})
