from manager.models import Item


def run():
    failed_items = (
        Item.objects.filter(cost__success=False)
        .exclude(cost__reason__in=["zeroquantity", "latestpriceiszero"])
        .select_related("cost")
        .order_by("ingredient__name")
    )
    return {
        "Items with Failed Cost Lookup": {
            "template": "manager/diagnostics/partials/cost_results_table.html",
            "data": [
                {
                    "item": item,
                    "price_unit": item.cost.price_unit,
                    "reason": item.cost.reason,
                }
                for item in failed_items
            ],
        }
    }
