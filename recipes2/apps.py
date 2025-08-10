from django.apps import AppConfig
import logging


class Recipes2Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes2"
    label = "manager" 
    
    def ready(self):
        import recipes2.signals
