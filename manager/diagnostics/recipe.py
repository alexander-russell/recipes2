from datetime import timedelta
from django.utils.timezone import now
from manager.models import Recipe
from django.db.models import Count


def run():
    old_threshold = now().date() - timedelta(days=60)

    return {
        "Missing Yield Quantity": Recipe.objects.filter(yield_quantity__isnull=True),
        "Missing Time Quantity": Recipe.objects.filter(time_quantity__isnull=True),
        "Recipes Not Updated Recently": Recipe.objects.filter(
            date_updated__lt=old_threshold
        ),
        "Untested Recipes": Recipe.objects.filter(tested=False),
        "Recipes Needing Revision": Recipe.objects.filter(needs_revision=True),
    }


from datetime import timedelta
from django.utils.timezone import now
from manager.models import Recipe


def run():
    old_threshold = now().date() - timedelta(days=60)

    return {
        "Missing Yield Quantity": {
            "template": "manager/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(yield_quantity__isnull=True),
        },
        "Missing Time Quantity": {
            "template": "manager/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(time_quantity__isnull=True),
        },
        "Recipes Not Updated Recently": {
            "template": "manager/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(date_updated__lt=old_threshold),
        },
        "Untested Recipes": {
            "template": "manager/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(tested=False),
        },
        "Recipes Needing Revision": {
            "template": "manager/diagnostics/partials/_results_table_recipe_base.html",
            "data": Recipe.objects.active().filter(needs_revision=True),
        },
    }