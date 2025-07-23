from collections import defaultdict
import os
from django.conf import settings
from django.http import HttpResponseBadRequest
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.templatetags.static import static
from manager.forms import SearchForm
from manager.models import Cuisine, Diary, Recipe
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.timezone import now


def home(request):
    recipes = (
        Recipe.objects.filter(status=Recipe.Status.ACTIVE)
        .only("name", "slug")
        .order_by("name")
    )
    return render(request, "manager/home/index.html", {"recipes": recipes})


def quick_search(request):
    recipes = (
        Recipe.objects.filter(status=Recipe.Status.ACTIVE)
        .only("name", "slug")
        .order_by("name")
    )
    return render(request, "manager/quick_search/index.html", {"recipes": recipes})


def index(request):
    index_entries = []  # defaultdict(list)
    recipes = Recipe.objects.filter(status=Recipe.Status.ACTIVE).select_related(
        "cuisine"
    )

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

    index_entries.sort(key=lambda x: (x["first_letter"], x["group"], x["name"]))

    return render(
        request,
        "manager/index/index.html",
        {"recipes": recipes, "index_entries": index_entries},
    )


def gallery(request):
    recipes = Recipe.objects.all()
    return render(request, "manager/gallery/index.html", {"recipes": recipes})


def explore(request):
    form = SearchForm(request.GET or None)
    recipes = (
        Recipe.objects
        .filter(status=Recipe.Status.ACTIVE)
        .select_related("cost__yield_unit", "yield_unit")
        .prefetch_related("images")
        .order_by("name")
    )

    # Ensure all recipes have a cost
    for recipe in recipes:
        recipe.get_cost()

    if form.is_valid():
        query = form.cleaned_data.get("query")

        if query:
            recipes = recipes.filter(name__icontains=query)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "manager/explore/partials/_results.html",
            {"recipes": recipes},
            request=request,
        )
        return JsonResponse({"html": html})

    return render(
        request, "manager/explore/index.html", {"form": form, "recipes": recipes}
    )


def contents(request):
    focus = request.GET.get("focus")
    recipes = (
        Recipe.objects.all()
        .filter(status=Recipe.Status.ACTIVE)
        .select_related("classification")
        .order_by(
            "classification__type__name", "classification__category__name", "name"
        )
        .select_related(
            "classification", "classification__type", "classification__category"
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


def viewer(request, recipe_slug):
    # Get recipe
    recipe = get_object_or_404(
        Recipe.objects.select_related(
            "classification",
            "classification__type",
            "classification__category",
            "yield_unit",
        ).prefetch_related(
            "items",
            "items__ingredient",
            "items__unit",
            "items__cost",
            "steps",
            "images",
            "timers",
            "diaryentries",
        ),
        slug=recipe_slug,
    )

    # Calculate costs
    item_costs = [item.get_cost() for item in recipe.items.all()]
    total_cost = sum(
        item_cost.amount if item_cost.amount is not None else 0
        for item_cost in item_costs
    )

    cost_per_serve = (
        total_cost / recipe.yield_quantity
        if recipe.yield_quantity is not None
        else None
    )

    # Get URL yield paramter if specified
    yield_param = request.GET.get("yield")

    # Determine if recipe hasn't been updated in over a month
    stale = recipe.date_updated < date.today() - timedelta(days=60)

    return render(
        request,
        "manager/viewer/index.html",
        {
            "recipe": recipe,
            "item_costs": item_costs,
            "total_cost": total_cost,
            "cost_per_serve": cost_per_serve,
            "stale": stale,
            "yield_param": yield_param,
        },
    )


def add_diary_entry(request, recipe_slug):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, slug=recipe_slug)
        content = request.POST.get("content")
        if not content:
            return HttpResponseBadRequest("Missing content")

        Diary.objects.create(recipe=recipe, date=now(), content=content)
        recipe.refresh_from_db()
        html = render_to_string(
            "manager/viewer/partials/_diary_overlay.html",
            {
                "diaryentries": recipe.diaryentries.all(),
                "overlay_name": "diary-overlay",
            },
        )
        return JsonResponse({"html": html})
    return HttpResponseBadRequest("Invalid request")
