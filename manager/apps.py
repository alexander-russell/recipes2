from django.apps import AppConfig
import logging

class ManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manager'

    def ready(self):
        logging.warning("Importing manager.signals")
        import manager.signals