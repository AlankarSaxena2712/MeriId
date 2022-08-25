from django.apps import AppConfig

from services.telegramService import get_current_data


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    def ready(self):
        from users.scheduler import scheduler
        scheduler.start()
        # get_current_data()

