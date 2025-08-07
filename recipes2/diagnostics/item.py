from recipes2.models import Item, Recipe


def run():
    failed_items = (
        Item.objects.filter(recipe__status=Recipe.Status.ACTIVE).filter(cost__success=False)
        .exclude(cost__reason__in=["zeroquantity", "latestpriceiszero"])
        .select_related("cost")
        .order_by("ingredient__name")
    )
    return {
        "No Cost": {
            "template": "recipes2/diagnostics/partials/_results_table_item_cost.html",
            "data": failed_items
        }
    }
