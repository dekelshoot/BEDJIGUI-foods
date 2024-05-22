from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
# Create your models here.


# class UserClient(AbstractUser):
#     nom = models.CharField(max_length=50)
#     email = models.EmailField()
#     telephone = models.CharField(max_length=12)
#     adresse = models.CharField(max_length=50)
#     photo = models.ImageField(blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
