# This file acts as a proxy to make models available at the standard
# 'users.models' path, as expected by Django for settings like AUTH_USER_MODEL
# and internal relations (e.g., in django.contrib.admin).

from .infrastructure.persistence.models import User, UserProfile

# Specify what gets imported with * (optional but good practice)
__all__ = ['User', 'UserProfile'] 