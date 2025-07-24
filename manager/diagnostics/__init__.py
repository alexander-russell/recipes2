from . import items, recipes, ingredients

def run_all():
    results = {}
    results.update(items.run())
    results.update(recipes.run())
    results.update(ingredients.run())
    return results