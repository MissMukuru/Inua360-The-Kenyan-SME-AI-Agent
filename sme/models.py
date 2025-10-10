from django.db import models

# Create your models here.

class SMEProfile(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    size = models.CharField(max_length=50)
    year_established = models.IntegerField()
    ownership_type = models.CharField(max_length=150)
    region = models.CharField(max_length=150)
    sector = models.CharField(max_length=150)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name