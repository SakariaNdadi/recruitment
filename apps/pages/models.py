from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    contact = PhoneNumberField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()