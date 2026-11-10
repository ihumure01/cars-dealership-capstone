
from django.db import models


class Dealer(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100, default="")

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_name} - {self.dealer.name}"
