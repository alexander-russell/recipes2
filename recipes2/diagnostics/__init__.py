from . import Item, Step, Recipe, Ingredient

def run_all():
    results = {}
    results.update(Item.run())
    results.update(Step.run())
    results.update(Recipe.run())
    results.update(Ingredient.run())
    return results