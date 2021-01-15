from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser


class ShortenUrl(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    parameter = models.CharField(max_length=50, unique=True)
    link = models.URLField(default='')

    def __str__(self):
        return self.parameter

    def get_absolute_url(self):
        return reverse('tds:short-url-view', kwargs={'pk': self.pk})


class MinMaxFloat(models.FloatField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(MinMaxFloat, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value' : self.max_value}
        defaults.update(kwargs)
        return super(MinMaxFloat, self).formfield(**defaults)


class RedirectLink(models.Model):
    parameter = models.ForeignKey(ShortenUrl,
                                  on_delete=models.CASCADE)
    url = models.URLField()
    country = CountryField(multiple=False, blank=True, null=True)
    weight = MinMaxFloat(min_value=0.0, max_value=1.0)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('tds:short-url-view', kwargs={'pk': self.parameter.id})


class UserClickStat(models.Model):
    ip = models.CharField(max_length=25)
    parameter = models.CharField(max_length=50)
    url_created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    url = models.URLField()
    time = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.ip} at {self.parameter}"


class AuthUser(AbstractUser):
    pass
