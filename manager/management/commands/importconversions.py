import csv
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from manager.models import Unit, Ingredient, Conversion

class Command(BaseCommand):
    help = 'Imports conversion rules from a CSV file'

    def handle(self, *args, **kwargs):
        # Path to the CSV file
        csv_file_path = 'C:/Users/alexa/Desktop/Phonebook/Databases/Recipes/conversions.csv'

        # Open the CSV file and read data
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Get or create from_unit and to_unit
                from_unit, created = Unit.objects.get_or_create(name=row['From'])
                to_unit, created = Unit.objects.get_or_create(name=row['To'])
                
                # Get or create ingredient (if applicable)
                ingredient = None
                if row['Item']:
                    ingredient, created = Ingredient.objects.get_or_create(name=row['Item'])

                # Create Conversion entry
                try:
                    conversion = Conversion(
                        from_unit=from_unit,
                        to_unit=to_unit,
                        factor=row['Factor'],
                        ingredient=ingredient
                    )
                    conversion.save()

                    print(f"Conversion created: {from_unit.name} -> {to_unit.name}, Factor: {conversion.factor}")
                except IntegrityError as e:
                    self.stderr.write(f"Error saving price for {name}: {e}")