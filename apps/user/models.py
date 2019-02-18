from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class SiteAdmin(AbstractUser):
    """
    网站管理员
    """
    def __str__(self):
        return str(self.username)
