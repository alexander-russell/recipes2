from collections import defaultdict
from django.http import Http404, HttpResponse
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.template import loader

from manager.models import Cuisine, Recipe


def home(request):
    recipes = Recipe.objects.all()
    return render(request, "manager/home/index.html", {"recipes": recipes})


def index(request):
    index_entries = []#defaultdict(list)
    recipes = Recipe.objects.filter(status=Recipe.Status.ACTIVE)

    # Collect all recipes
    for recipe in recipes:
        index_entries.append(
            {
                "first_letter": recipe.name[0].upper(),
                "group": recipe.name,
                "name": None,
                "slug": recipe.slug,
            }
        )

        if recipe.cuisine is not None:
            index_entries.append(
                {
                    "first_letter": recipe.cuisine.name[0].upper(),
                    "group": recipe.cuisine.name,
                    "name": recipe.name,
                    "slug": recipe.slug,
                }
            )

        if recipe.vegetarian:
            index_entries.append(
                {
                    "first_letter": "V",
                    "group": "Vegetarian",
                    "name": recipe.name,
                    "slug": recipe.slug,
                }
            )

    index_entries.sort(key=lambda x: (x['first_letter'], x['group'], x['name']))

    return render(request, "manager/index/index.html", {"recipes": recipes, "index_entries": index_entries})


def gallery(request):
    recipes = Recipe.objects.all()
    return render(request, "manager/gallery/index.html", {"recipes": recipes})


def explore(request):
    recipes = Recipe.objects.all()
    return render(request, "manager/explore/index.html", {"recipes": recipes})


def contents(request):
    focus = request.GET.get("focus")
    recipes = (
        Recipe.objects.all()
        .filter(status=Recipe.Status.ACTIVE)
        .select_related("classification")
        .order_by(
            "classification__type__name", "classification__category__name", "name"
        )
    )

    grouped = defaultdict(lambda: defaultdict(list))
    for recipe in recipes:
        type_ = recipe.classification.type
        category = recipe.classification.category
        grouped[type_][category].append(recipe)

    return render(
        request,
        "manager/contents/index.html",
        {"recipes": recipes, "grouped_recipes": grouped, "focus": focus},
    )


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
