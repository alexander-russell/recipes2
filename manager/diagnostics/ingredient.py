from manager.models import Ingredient

def run():
    return {
        "Ingredients Missing Price Records": {
            "template": "manager/diagnostics/partials/results_list.html",
            "data": Ingredient.objects.filter(prices__isnull=True),
        }
    }