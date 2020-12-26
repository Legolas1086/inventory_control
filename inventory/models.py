from django.db import models

# Create your models here.

class user(models.Model):
    username = models.CharField(max_length=25,blank=False)
    password = models.CharField(max_length=25,blank=False)