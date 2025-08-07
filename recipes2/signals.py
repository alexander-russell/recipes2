from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import IngredientPrice, Item, ItemCost, ItemGroup, Recipe, Step, StepGroup, Tag, Timer

import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Item)
@receiver(post_delete, sender=Item)
@receiver(post_save, sender=Step)
@receiver(post_delete, sender=Step)
@receiver(post_save, sender=ItemGroup)
@receiver(post_delete, sender=ItemGroup)
@receiver(post_save, sender=StepGroup)
@receiver(post_delete, sender=StepGroup)
@receiver(post_save, sender=Timer)
@receiver(post_delete, sender=Timer)
@receiver(post_save, sender=Tag)
@receiver(post_delete, sender=Tag)
def related_model_changed(sender, instance, **kwargs):
    logger.warning(f"Signal (related_model_changed) fired for {sender.__name__} with instance {instance}")
    Recipe.objects.filter(pk=instance.recipe.pk).update(date_updated=timezone.now())

@receiver(post_save, sender=Recipe)
def recipe_changed(sender, instance, **kwargs):
    logger.warning(f"Signal (recipe_changed) fired for {sender.__name__} with instance {instance}")
    Recipe.objects.filter(pk=instance.pk).update(date_updated=timezone.now())

@receiver(post_save, sender=Item)
def update_item_cost_on_item_change(sender, instance, **kwargs):
    logger.warning(f"Signal (update_item_cost_on_item_change) fired for {sender.__name__} with instance {instance}")
    instance.update_cost()

@receiver(post_save, sender=IngredientPrice)
def refresh_item_costs_on_ingredient_price_change(sender, instance, **kwargs):
    logger.warning(f"Signal (refresh_item_costs_on_ingredient_price_change) fired for {sender.__name__} with instance {instance}")
    for item in Item.objects.filter(ingredient=instance.ingredient):
        item.update_cost()

@receiver(post_save, sender=ItemCost)
def update_recipe_cost_on_item_cost_change(sender, instance, **kwargs):
    logger.warning(f"Signal (update_recipe_cost_on_item_cost_change) fired for {sender.__name__} with instance {instance}")
    recipe = instance.item.recipe
    recipe.update_cost()