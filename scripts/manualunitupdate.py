# Get the 'manual' unit instance
manual_unit = Unit.objects.get(singular="manual")

# Filter items with quantity 0, non-blank unit_detail, and unit not 'manual'
items_to_update = Item.objects.filter(quantity=0)\
    .exclude(unit__singular="manual")

for item in items_to_update:
    old_unit_name = item.unit.singular
    print(f"\nItem ID: {item.id}, Ingredient: {item.ingredient.name}")
    print(f"Quantity: {item.quantity}, Current unit: {old_unit_name}")
    print(f"Proposed change: unit -> 'manual', unit_detail -> '{old_unit_name}'")

    item.unit_detail = old_unit_name
    item.unit = manual_unit
    item.save()
    print("Updated.\n")

print("Done.")
