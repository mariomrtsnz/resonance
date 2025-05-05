from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"

    def ready(self):
        from .containers import ProjectContainer
        self.container = ProjectContainer()
        self.container.wire(modules=[".infrastructure.api.views"])
