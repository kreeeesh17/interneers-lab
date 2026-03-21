from django.apps import AppConfig
from .db_connection import initialize_mongo


class Week4Config(AppConfig):
    name = "week4"

    def ready(self):
        initialize_mongo()
