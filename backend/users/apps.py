from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        """Called when Django starts. Used here to initialize DI container."""
        # Imports are local to prevent AppRegistryNotReady errors
        from .containers import UserContainer
        # Ensure infrastructure modules are loaded for wiring
        from . import infrastructure

        self.container = UserContainer()

        self.container.wire(
            # List modules where @inject or Provide is used
            modules=[
                "users.infrastructure.api.views",
            ]
        )
