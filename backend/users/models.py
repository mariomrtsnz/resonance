from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # Add additional fields here in the future if needed
    pass

    def __str__(self):
        return self.username 

class UserProfile(models.Model):
    class CollaborationStatusChoices(models.TextChoices):
        OPEN_TO_HELP = 'OPEN', _('Open to Help')
        NEEDS_HELP = 'NEEDS', _('Needs Help')
        NOT_LOOKING = 'NONE', _('Not Looking')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'  # Allows accessing profile via user.profile
    )
    bio = models.TextField(_('bio'), blank=True)
    location = models.CharField(_('location'), max_length=255, blank=True)
    collaboration_status = models.CharField(
        _('collaboration status'),
        max_length=5,
        choices=CollaborationStatusChoices.choices,
        default=CollaborationStatusChoices.NOT_LOOKING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Profile" 