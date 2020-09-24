"""
from django.db import models

# Create your models here.

class Shift(models.Model):
	group = models.CharField(max_length=100, primary_key=True)
	shift = models.CharField(max_length=400, null=True, blank=True)
	candidate = models.CharField(max_length=500, null=True, blank=True)
	update_at = models.DateTimeField(auto_now=True)

"""