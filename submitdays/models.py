from django.db import models
from django.conf import settings

ROLE_CHOICES = (
    ('1', 'キッチン'),
    ('2', 'ホール'),
    ('3', '両方')
)


class Profile(models.Model):
    name = models.CharField(max_length=1)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    group = models.CharField(max_length=100, null=True, blank=True)
    days = models.CharField(max_length=100, null=True, blank=True)
    morethan =  models.BooleanField(default=False)
    update_at = models.DateTimeField(auto_now=True) 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

