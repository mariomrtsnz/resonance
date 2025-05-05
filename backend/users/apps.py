from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        # Imports are local to prevent AppRegistryNotReady errors
        from .containers import UserContainer
        self.container = UserContainer()
        self.container.wire(
            modules=[
                ".infrastructure.api.views",
            ]
        )
