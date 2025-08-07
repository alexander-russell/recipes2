from recipes2.models import Ingredient, Recipe

def run():
    return {
        "No Price": {
            "template": "recipes2/diagnostics/partials/_results_table_ingredient_base.html",
            "data": Ingredient.objects.filter(items__recipe__status=Recipe.Status.ACTIVE, items__quantity__gt=0).filter(prices__isnull=True).distinct(),
        }
    }