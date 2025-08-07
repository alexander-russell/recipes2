import json
from zoneinfo import ZoneInfo
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from recipes2.models import (
    Timer, Type, Category, Classification, YieldUnit, Cuisine,
    Recipe, Ingredient, Unit, ItemGroup, Item, Step, Diary
)
from django.db import IntegrityError

User = get_user_model()

sydney_tz = ZoneInfo("Australia/Sydney")

class Command(BaseCommand):
    help = 'Imports recipes from JSON file'

    def handle(self, *args, **kwargs):
        # Assuming the JSON file is in the same directory as the script
        with open('C:/Users/alexa/Desktop/Phonebook/Databases/Recipes/Recipes.json') as f:
            data = json.load(f)

        # print(type(data))  # Should be <class 'list'>, if it's a list of recipes
        # # print(data)
        # for entry in data.get("Recipes"):
        #     print(entry)
        #     break

        for entry in data.get("Recipes"):
            if Recipe.objects.filter(slug=entry["Slug"]).exists():
                print(f"Recipe with slug '{entry['Slug']}' already exists. Skipping creation.")
                continue  # Skip the current iteration if the recipe exists

            try:
                # Ensure Type/Category/Classification exists or create it
                type_name = entry["Type"]
                category_name = entry["Category"]

                type_instance, created = Type.objects.get_or_create(name=type_name)
                category_instance, created = Category.objects.get_or_create(name=category_name)
                
                classification_instance, created = Classification.objects.get_or_create(
                    type=type_instance, category=category_instance
                )

                # Ensure Cuisine exists or create it
                cuisine_name = entry["Cuisine"]
                cuisine_instance, created = Cuisine.objects.get_or_create(name=cuisine_name)

                # Ensure YieldUnit exists or create it (assuming a unit like "serves", "whole", etc.)
                yield_unit_name = entry["Yield"]["Unit"]
                yield_unit_instance, created = YieldUnit.objects.get_or_create(name=yield_unit_name)

                # Prepare Recipe data and create it
                recipe = Recipe(
                    name=entry["Name"],
                    slug=entry["Slug"],
                    classification=classification_instance,
                    date_created = entry.get("DateCreated") or timezone.now(),
                    date_updated = entry.get("DateUpdated") or timezone.now(),
                    status=Recipe.Status.ACTIVE if not entry.get("Retired", False) else Recipe.Status.ARCHIVED,
                    needs_revision=entry["NeedsRevision"],
                    yield_quantity=entry["Yield"]["Quantity"] if entry["Yield"]["Quantity"] != 0 else None,
                    yield_unit=yield_unit_instance,
                    yield_detail=entry["Yield"].get("Extra", ""),
                    time_quantity=timedelta(minutes=entry["Time"]["Minutes"]) if entry["Time"]["Minutes"] != 0 else None,
                    time_detail=entry["Time"].get("Extra", ""),
                    difficulty=entry.get("Difficulty", None),
                    bulk=entry["Bulk"],
                    favourite=entry["Favourite"],
                    tested=entry["Tested"],
                    vegetarian=entry["Dietary"]["Vegetarian"],
                    vegan=entry["Dietary"]["Vegan"],
                    gluten_free=entry["Dietary"]["GlutenFree"],
                    cuisine=cuisine_instance,
                    description=entry.get("Note", "")
                )
                recipe.save()

                # Handle Items (with ItemGroups)
                item_groups = {}  # Dictionary to store unique ItemGroups for this recipe
                for item_data in entry["Items"]:
                    # Ensure Ingredient exists or create it
                    ingredient_name = item_data["Name"]
                    ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)

                    # Ensure Unit exists or create it
                    unit_name = item_data["Unit"]
                    unit, created = Unit.objects.get_or_create(name=unit_name)

                    # Handle ItemGroup creation if a group exists for this item
                    group_name = item_data["Group"]
                    if group_name:
                        if group_name not in item_groups:
                            item_group = ItemGroup.objects.create(recipe=recipe, name=group_name)
                            item_groups[group_name] = item_group
                        group = item_groups[group_name]
                    else:
                        group = None

                    # Create Item for the recipe
                    item = Item(
                        recipe=recipe,
                        position=entry["Items"].index(item_data),
                        ingredient=ingredient,
                        ingredient_detail=item_data.get("NameDetail", ""),
                        quantity=item_data["Quantity"],
                        unit=unit,
                        unit_detail=item_data.get("UnitDetail", ""),
                        group=group
                    )
                    item.save()

                # Handle Steps
                for step_data in entry["Steps"]:
                    step = Step(
                        recipe=recipe,
                        position=entry["Steps"].index(step_data),
                        content=step_data["Content"]
                    )
                    step.save()

                # Handle Diary Entries
                for diary_data in (entry.get("Diary") or [] if entry.get("Diary") != "null" else []):
                    diary_entry = Diary(
                        recipe=recipe,
                        date=datetime.fromisoformat(diary_data["Date"]).replace(tzinfo=sydney_tz),
                        user=User.objects.get(id=1),
                        content=diary_data["Content"]
                    )
                    diary_entry.save()

                # Handle Timers (if necessary, not explicitly mapped in your models, but added for completeness)
                for timer_data in entry.get("Timers", []):
                    # Assuming no explicit Timer model, just a dummy implementation
                    timer = Timer(
                        recipe=recipe,
                        position=entry.get("Timers", []).index(timer_data),
                        name=timer_data["Name"],
                        duration=timedelta(seconds=timer_data["Seconds"])
                    )
                    timer.save()

                # Optionally handle cost calculation, images, etc. later
                print(f"Recipe '{recipe.name}' has been added.")
            except IntegrityError as e:
                self.stderr.write(f"Error saving price for {entry["Name"]}: {e}")
