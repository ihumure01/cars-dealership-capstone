
from django.db import models


class Dealer(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    st = models.CharField(max_length=10, blank=True, default="")
    address = models.CharField(max_length=255, blank=True, default="")
    zip = models.CharField(max_length=20, blank=True, default="")
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    short_name = models.CharField(max_length=150, blank=True, default="")
    full_name = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.name


class Review(models.Model):
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    reviewer_name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True, default="")
    car_model = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_name} - {self.dealer.name}"


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="models"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
