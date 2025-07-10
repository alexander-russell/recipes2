from threading import Timer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Item, ItemGroup, Recipe, Step, StepGroup, Tag

@receiver(post_save, sender=Item)
@receiver(post_delete, sender=Item)
@receiver(post_save, sender=Step)
@receiver(post_delete, sender=Step)
@receiver(post_save, sender=Recipe)
@receiver(post_delete, sender=Recipe)
@receiver(post_save, sender=ItemGroup)
@receiver(post_delete, sender=ItemGroup)
@receiver(post_save, sender=StepGroup)
@receiver(post_delete, sender=StepGroup)
@receiver(post_save, sender=Timer)
@receiver(post_delete, sender=Timer)
@receiver(post_save, sender=Tag)
@receiver(post_delete, sender=Tag)
def related_model_changed(sender, instance, **kwargs):
    recipe = instance if isinstance(instance, Recipe) else instance.recipe
    recipe.date_updated = timezone.now()
    recipe.save(update_fields=['date_updated'])