from django.core.management.base import BaseCommand
from recipes2.models import Recipe, Ingredient

class Command(BaseCommand):
    help = "Run all recipe data quality checks"

    def handle(self, *args, **kwargs):
        self.check_missing_yield()
        self.check_ingredients_missing_price()

    def check_missing_yield(self):
        missing = Recipe.objects.filter(yield_quantity__isnull=True)
        self.stdout.write("\n[Missing Yield Quantity]")
        for recipe in missing:
            self.stdout.write(f"- {recipe.name} (ID: {recipe.id})")
        self.stdout.write(f"Total: {missing.count()}")

    def check_ingredients_missing_price(self):
        missing = Ingredient.objects.filter(prices__isnull=True)
        self.stdout.write("\n[Ingredients Missing Price Data]")
        for ingredient in missing:
            self.stdout.write(f"- {ingredient.name} (ID: {ingredient.id})")
        self.stdout.write(f"Total: {missing.count()}")