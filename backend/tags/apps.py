from django.apps import AppConfig

class TagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tags'
    verbose_name = 'Tags'

    def ready(self):
        from .containers import SkillContainer
        self.container = SkillContainer()
        self.container.wire(modules=[".infrastructure.api.views"])