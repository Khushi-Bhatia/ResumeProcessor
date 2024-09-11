from django.db import models

# Create your models here.
class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
         return f'{self.first_name} ({self.email})'

