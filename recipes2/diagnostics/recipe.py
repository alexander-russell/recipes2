from datetime import timedelta
from django.utils.timezone import now
from recipes2.models import Recipe
from django.db.models import Count


def run():
    old_threshold = now().date() - timedelta(days=60)

    return {
        "No Yield Quantity": {
            "template": "recipes2/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(yield_quantity__isnull=True),
        },
        "No Time Quantity": {
            "template": "recipes2/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(time_quantity__isnull=True),
        },
        "Stale": {
            "template": "recipes2/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(date_updated__lt=old_threshold),
        },
        "Untested": {
            "template": "recipes2/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(tested=False),
        },
        "Marked For Revision": {
            "template": "recipes2/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(needs_revision=True),
        },
        "Recipes Missing Main Image": {
            "template": "recipes2/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().exclude(images__name="main"),
        },
        "Only Recipe in Classification": {
            "template": "recipes2/diagnostics/partials/_results_table_recipe_classification.html",
            "data": (
                Recipe.objects.active()
                .annotate(
                    recipe_in_classification_count=Count("classification__recipes")
                )
                .filter(recipe_in_classification_count=1)
            ),
        },
        "Recipes In Draft": {
            "template": "recipes2/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.filter(status=Recipe.Status.DRAFT),
        },
    }
