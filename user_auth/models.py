from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class User_Auth(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super(User_Auth, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
