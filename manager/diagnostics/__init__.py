from . import item, recipe, ingredient

def run_all():
    results = {}
    results.update(item.run())
    results.update(recipe.run())
    results.update(ingredient.run())
    return results