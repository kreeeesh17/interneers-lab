from django.apps import AppConfig
from .db_connection import initialize_mongo


class Week3Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "week3"

    def ready(self):
        initialize_mongo()
