from django.urls import path
from . import views

urlpatterns = [
    path("post-review/", views.post_review, name="post-review"),
    path("api/analyze-review/", views.analyze_review, name="analyze-review"),
    path("api/car-makes/", views.get_all_car_makes, name="all-car-makes"),
    path("", views.home, name="home"),
    path("djangoapp/login", views.djangoapp_login, name="djangoapp-login"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("api/dealers/<int:dealer_id>/reviews/", views.get_dealer_reviews, name="dealer-reviews"),
    path("api/dealers/", views.get_all_dealers, name="all-dealers"),
    path("api/dealers/state/kansas/", views.get_dealers_by_state, name="dealers-by-state"),
    path("api/dealers/<int:dealer_id>/", views.get_dealer_by_id, name="dealer-by-id"),
]
