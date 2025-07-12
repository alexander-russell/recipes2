from django.http import Http404, HttpResponse
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.template import loader

from manager.models import Recipe


def index(request):
    return HttpResponse(
        "Hello, world. You're at the manager index. <a href=" "contents" ">hey</a>"
    )


def contents(request):
    all_recipes = Recipe.objects.all()
    context = {"all_recipes": all_recipes}
    return render(request, "manager/contents/index.html", context)


def view(request, recipe_slug):
    # Get recipe
    recipe = get_object_or_404(Recipe, slug=recipe_slug)

    # Calculate costs
    item_costs = [item.get_cost() for item in recipe.items.all()]
    total_cost = sum(
        item_cost["amount"] if item_cost["amount"] is not None else 0
        for item_cost in item_costs
    )
    cost_per_serve = total_cost / recipe.yield_quantity

    # Determine if recipe hasn't been updated in over a month
    stale = recipe.date_updated < date.today() - timedelta(days=60)

    return render(
        request,
        "manager/view/index.html",
        {
            "recipe": recipe,
            "item_costs": item_costs,
            "total_cost": total_cost,
            "cost_per_serve": cost_per_serve,
            "stale": stale,
        },
    )
