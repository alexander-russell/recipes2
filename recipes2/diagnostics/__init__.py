from . import item, step, recipe, ingredient

def run_all():
    results = {}
    results.update(item.run())
    results.update(step.run())
    results.update(recipe.run())
    results.update(ingredient.run())
    return results