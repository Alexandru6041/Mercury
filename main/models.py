from django.db import models

# Create your models here.
class User(models.Model):
    
    #Credentials
    username = models.CharField(max_length = 256) #sha-256
    password = models.CharField(max_length = 256) #sha-256
    email = models.EmailField()
    
    display_name = models.CharField(max_length = 64)
    counter = models.IntegerField(editable = True)