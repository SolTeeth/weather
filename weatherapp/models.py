from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    cities = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'User info'
        verbose_name_plural = 'Users'' info'
