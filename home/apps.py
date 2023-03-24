from django.apps import AppConfig


class FrontpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
class HomeConfig(AppConfig):
    name = 'home'
    def ready(self):
        import home.management.commands.create_room_number
