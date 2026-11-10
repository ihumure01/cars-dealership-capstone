from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("api/dealers/<int:dealer_id>/reviews/", views.get_dealer_reviews, name="dealer-reviews"),
    path("api/dealers/", views.get_all_dealers, name="all-dealers"),
]
