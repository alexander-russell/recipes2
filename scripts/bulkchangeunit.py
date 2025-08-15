from recipes2.models import Item, Unit

# Get the "cup" unit object (singular form)
new_unit = Unit.objects.filter(singular="clove").first()
if not new_unit:
    raise ValueError("New unit not found")

# Find and update all items that currently use "cups"
old_unit = Unit.objects.filter(singular="cloves").first()
if not old_unit:
    raise ValueError("Old unit not found")

# Bulk update
updated_count = Item.objects.filter(unit=old_unit).update(unit=new_unit)
print(f"Updated {updated_count} items from {old_unit.singular} to {new_unit.singular}")
