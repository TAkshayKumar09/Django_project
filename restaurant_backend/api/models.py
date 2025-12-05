from django.db import models

# Create your models here.

class users(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    mobile=models.CharField(max_length=10, unique=True)
    password=models.CharField(max_length=255)


class fooditems(models.Model):
    name=models.CharField(max_length=200, unique=True)
    description=models.CharField(max_length=200)
    price=models.CharField(max_length=10)
    image=models.URLField(default="empty")
    category=models.CharField(max_length=50)