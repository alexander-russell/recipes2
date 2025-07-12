import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from manager.models import Ingredient, Unit, IngredientSource, IngredientPrice
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Imports ingredients and their prices from a CSV file'

    def handle(self, *args, **kwargs):
        # Assuming the CSV file is located at the absolute path
        csv_file_path = 'C:/Users/alexa/Desktop/Phonebook/Databases/Recipes/ingredients.csv'

        # Open and read the CSV file
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Parse fields
                    date_str = row['Date']
                    name = row['Name']
                    price = row['Price']
                    quantity = row['Quantity']
                    unit_name = row['Unit']
                    source_name = row['Source']
                    detail = row['Extra']  # This is renamed to 'detail'

                    # Parse the date field
                    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

                    # Get or create Ingredient
                    ingredient, created = Ingredient.objects.get_or_create(name=name)

                    # Get or create Unit
                    unit, created = Unit.objects.get_or_create(name=unit_name)

                    # Get or create IngredientSource
                    ingredient_source, created = IngredientSource.objects.get_or_create(name=source_name)

                    # Create IngredientPrice entry
                    try:
                        ingredient_price = IngredientPrice(
                            ingredient=ingredient,
                            date=date,
                            price=price,
                            quantity=quantity,
                            unit=unit,
                            source=ingredient_source,
                            detail=detail
                        )
                        ingredient_price.save()
                        self.stdout.write(f"IngredientPrice for {ingredient.name} on {date} saved.")
                    except IntegrityError as e:
                        self.stderr.write(f"Error saving price for {name}: {e}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to process CSV file: {str(e)}"))
