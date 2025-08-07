from django.apps import AppConfig
import logging


class Recipes2Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes2"

    def ready(self):
        logging.warning("Importing recipes2.signals")
        import recipes2.signals
