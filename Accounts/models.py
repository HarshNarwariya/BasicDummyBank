from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountDetail(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    total_deposited = models.IntegerField(default=0)
    total_withdrawl = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.balance)