import uuid
from django.db import models


# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ("shoes", "Shoes"),
        ("ball", "Ball"),
        ("jersey", "Jersey"),
        ("tradingcard", "Trading Card"),
        ("other", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )
    is_featured = models.BooleanField(default=False)
    rating = models.FloatField(default=0)


def __str__(self):
    return self.title