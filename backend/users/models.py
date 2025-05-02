from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add additional fields here in the future if needed
    pass

    def __str__(self):
        return self.username 