from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Record(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(null=False)
    D_CHOICES = (
        (True, 'Deposite'),
        (False, 'Withdrawl'),
    )
    is_deposited = models.BooleanField(choices=D_CHOICES)
    description = models.TextField(default="")
    total = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-transaction_date']