# This file acts as a proxy to make models available at the standard
# 'projects.models' path, as expected by Django internal mechanisms.

from .infrastructure.persistence.models import Project

__all__ = ['Project'] 