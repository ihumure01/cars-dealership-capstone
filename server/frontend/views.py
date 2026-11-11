from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Dealer, CarMake, Review
from .sentiment_analyzer import sentiment_analyzer
import json


def home(request):
    state = request.GET.get("state", "")
    dealers = Dealer.objects.all()
    if state:
        dealers = dealers.filter(state__iexact=state)
    states = Dealer.objects.exclude(state="").values_list("state", flat=True).distinct()
    return render(request, "frontend/home.html", {"dealers": dealers, "states": states, "selected_state": state})


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
def djangoapp_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": user.username,
                "status": "Authenticated"
            })

        return JsonResponse({"status": "Not Authenticated"}, status=401)

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
            "name": review.reviewer_name,
            "reviewer_name": review.reviewer_name,
            "dealership": dealer.id,
            "review": review.comment,
            "comment": review.comment,
            "rating": review.rating,
            "purchase": review.purchase,
            "purchase_date": (
                review.purchase_date.isoformat()
                if review.purchase_date else None
            ),
            "car_make": review.car_make,
            "car_model": review.car_model,
            "created_at": review.created_at.isoformat()
        }
        for review in reviews
    ]

    return JsonResponse({"reviews": data})



def get_all_dealers(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    dealers = Dealer.objects.all().order_by("id")
    data = [
        {
            "id": dealer.id,
            "name": dealer.name,
            "city": dealer.city,
            "state": dealer.state,
            "st": dealer.st,
            "address": dealer.address,
            "zip": dealer.zip,
            "lat": dealer.lat,
            "long": dealer.long,
            "short_name": dealer.short_name,
            "full_name": dealer.full_name,
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
        "name": dealer.name,
        "city": dealer.city,
        "state": dealer.state,
        "st": dealer.st,
        "address": dealer.address,
        "zip": dealer.zip,
        "lat": dealer.lat,
        "long": dealer.long,
        "short_name": dealer.short_name,
        "full_name": dealer.full_name,
    })



def get_dealers_by_state(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    dealers = Dealer.objects.filter(state__iexact="Kansas").order_by("id")

    data = [
        {
            "id": dealer.id,
            "name": dealer.name,
            "city": dealer.city,
            "state": dealer.state,
            "st": dealer.st,
            "address": dealer.address,
            "zip": dealer.zip,
            "lat": dealer.lat,
            "long": dealer.long,
            "short_name": dealer.short_name,
            "full_name": dealer.full_name,
        }
        for dealer in dealers
    ]

    return JsonResponse({"dealers": data})



def get_all_car_makes(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    makes = CarMake.objects.prefetch_related("models").all()

    data = [
        {
            "id": make.id,
            "name": make.name,
            "models": [
                {"id": car_model.id, "name": car_model.name}
                for car_model in make.models.all()
            ]
        }
        for make in makes
    ]

    return JsonResponse({"car_makes": data})


def get_cars(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    car_models = [
        {
            "CarMake": make.name,
            "CarModel": car_model.name
        }
        for make in CarMake.objects.prefetch_related("models").all()
        for car_model in make.models.all()
    ]

    return JsonResponse({"CarModels": car_models})


def analyze_review_get(request, review_text):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    result = sentiment_analyzer(review_text)
    return JsonResponse(result)

@csrf_exempt
def analyze_review(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        review_text = data.get("review", "")
        if not review_text:
            return JsonResponse({"error": "Review text is required"}, status=400)
        result = sentiment_analyzer(review_text)
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


def post_review(request):
    dealers = Dealer.objects.all()
    error = ""
    if request.method == "POST":
        dealer_id = request.POST.get("dealer")
        reviewer_name = request.POST.get("reviewer_name", "").strip()
        comment = request.POST.get("comment", "").strip()
        try:
            rating = int(request.POST.get("rating", "0"))
        except ValueError:
            rating = 0
        if not reviewer_name or not comment or not dealer_id or rating not in range(1, 6):
            error = "Please complete all fields and select a rating from 1 to 5."
        else:
            dealer = get_object_or_404(Dealer, id=dealer_id)
            Review.objects.create(dealer=dealer, reviewer_name=reviewer_name, comment=comment, rating=rating)
            return render(request, "frontend/post_review.html", {"dealers": dealers, "success": True})
    return render(request, "frontend/post_review.html", {"dealers": dealers, "error": error})


@csrf_exempt
def djangoapp_logout(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    logout(request)
    return JsonResponse({"userName": ""})
