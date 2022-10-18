from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Income(models.Model):
    amount = models.FloatField() # Decimal has more functionality than float
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self):
        return str(self.description)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Income'

class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']