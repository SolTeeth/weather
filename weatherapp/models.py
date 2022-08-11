from django.db import models
from django.contrib.auth.models import User


class Cities(models.Model):
    city = models.CharField(max_length=100, unique=True)

    @classmethod
    def add(cls, city):
        city_name = cls(city=city)
        return city_name

    def __str__(self):
        return self.city


class UserInfo(models.Model):
    cities = models.ManyToManyField(Cities)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'User info'
        verbose_name_plural = 'Users info'
