from recipes2.models import Item, Recipe
from django.db.models import F


def run():
    return {
        "No Cost": {
            "template": "recipes2/diagnostics/partials/_results_table_item_cost.html",
            "data": (
                Item.objects.filter(recipe__status=Recipe.Status.ACTIVE)
                .filter(cost__success=False)
                .exclude(cost__reason__in=["zeroquantity", "latestpriceiszero"])
                .select_related("cost")
                .order_by("ingredient__name")
            ),
        },
        "Group Recipe Mismatch": {
            "template": "recipes2/diagnostics/partials/_results_table_item_group.html",
            "data": (
                Item.objects.filter(recipe__status=Recipe.Status.ACTIVE)
                .exclude(group__isnull=True)
                .exclude(recipe__id=F("group__recipe__id"))
            ),
        },
        "Zero Quantity But Unit Not Manual": {
            "template": "recipes2/diagnostics/partials/_results_table_item_unit.html",
            "data": (
                Item.objects.filter(recipe__status=Recipe.Status.ACTIVE)
                .filter(quantity=0)
                .exclude(unit__name="manual")
            ),
        },
    }
