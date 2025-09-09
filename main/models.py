from django.db import models

# Create your models here.
class Product(models.model):
    name = models.CharField()
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField()
    is_featured = models.BooleanField()
    rating = models.FloatField()
    
    