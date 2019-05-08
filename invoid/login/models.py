from django.contrib.auth.models import AbstractUser
from django.db import models

class inVoidUsers(AbstractUser):
    authkey = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

