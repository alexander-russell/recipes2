from collections import defaultdict
import os
from django.conf import settings
from django.http import HttpResponseBadRequest
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.templatetags.static import static
import manager.diagnostics as diagnostics
from manager.forms import IngredientPriceForm, SearchForm
from manager.models import Cuisine, Diary, Ingredient, IngredientPrice, Recipe
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.middleware.csrf import get_token
from django.db.models import Q

def home(request):
    recipes = Recipe.objects.active().only("name", "slug").order_by("name")
    return render(request, "manager/home/index.html", {"recipes": recipes})


def quick_search(request):
    recipes = (
        Recipe.objects.exclude(status=Recipe.Status.ARCHIVED)
        .only("name", "slug")
        .order_by("name")
    )
    return render(request, "manager/quick_search/index.html", {"recipes": recipes})


def index(request):
    index_entries = []  # defaultdict(list)
    recipes = Recipe.objects.active().select_related("cuisine")

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
        Recipe.objects.active()
        .select_related("cost__yield_unit", "yield_unit")
        .prefetch_related("images")
        .order_by("name")
    )

    # Get results
    if form.is_valid():
        query = form.cleaned_data.get("query")
        search_scope = form.cleaned_data.get("search_scope", "title")
        if query:
            if search_scope == "title":
                recipes = recipes.filter(name__icontains=query)
            else:  # everywhere
                # Search in name OR description OR steps.content OR items.ingredient__name
                recipes = recipes.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(steps__content__icontains=query) |
                    Q(items__ingredient__name__icontains=query)
                ).distinct()

        # Filter by type and category via Classification (join)
        if form.cleaned_data.get("type"):
            recipes = recipes.filter(classification__type=form.cleaned_data["type"])

        if form.cleaned_data.get("category"):
            recipes = recipes.filter(classification__category=form.cleaned_data["category"])

        # Dietary filters
        if form.cleaned_data.get("vegetarian"):
            recipes = recipes.filter(vegetarian=True)

        if form.cleaned_data.get("vegan"):
            recipes = recipes.filter(vegan=True)

        if form.cleaned_data.get("gluten_free"):
            recipes = recipes.filter(gluten_free=True)

        # Cuisine filter
        if form.cleaned_data.get("cuisine"):
            recipes = recipes.filter(cuisine=form.cleaned_data["cuisine"])

        # Sorting
        sort = form.cleaned_data.get("sort", "name")
        sort_dir = form.cleaned_data.get("sort_direction", "asc")
        
        # Determine sort field
        if sort == "time_quantity":
            sort_field = "time_quantity"
        elif sort == "difficulty":
            sort_field = "difficulty"
        elif sort == "cost":
            sort_field = "cost__total"
        elif sort == "cost_per_serve":
            # cost per serve uses amount_per_unit, join on cost and yield_unit
            sort_field = "cost__amount_per_unit"
        else:
            sort_field = "name"

        # Prefix with '-' if descending
        if sort_dir == "desc":
            sort_field = "-" + sort_field

        recipes = recipes.order_by(sort_field)


    # Ensure all recipes have a cost
    for recipe in recipes:
        recipe.get_cost()

    # Render template (partial for htmx request, whole thing otherwise)
    if request.headers.get("Hx-Request"):
        return render(
            request, "manager/explore/partials/_results.html", {"recipes": recipes}
        )
    else:
        return render(
            request, "manager/explore/index.html", {"form": form, "recipes": recipes}
        )

def gallery(request):
    recipes = Recipe.objects.active().prefetch_related('images')

    images = []
    for recipe in recipes:
        first_image = recipe.images.first()
        if first_image:
            images.append({
                'slug': recipe.slug,
                'image_url': first_image.image.url,
                'alt_text': first_image.alt_text,
            })

    context = {
        'images': images,
    }
    return render(request, 'manager/gallery/index.html', context)

def contents(request):
    focus = request.GET.get("focus")
    recipes = (
        Recipe.objects.active()
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
        )
        .prefetch_related(
            "items",
            "items__ingredient",
            "items__unit",
            "items__cost",
            "steps",
            "images",
            "timers",
            "diaryentries",
        )
        .exclude(status=Recipe.Status.ARCHIVED),
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

@login_required
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@login_required
def accounts_login_success(request):
    return render(request, "manager/accounts/login/success/index.html")

def add_diary_entry(request, recipe_slug):
    if request.method == "POST":
        if not request.user.has_perm("manager.add_diary"):
            return JsonResponse({
                "success": False,
                "reason": "lackspermission"
            }, status=403)
        
        recipe = get_object_or_404(Recipe, slug=recipe_slug)
        content = request.POST.get("content")
        if not content:
            return HttpResponseBadRequest("Missing content")

        Diary.objects.create(recipe=recipe, date=now(), content=content, user=request.user)
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


def add_ingredient_price(request):
    # Use form data and save date in session
    if request.method == "POST":
        form = IngredientPriceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingredient price added.")
            request.session["last_price_date"] = form.cleaned_data["date"].isoformat()

    # Construct form with date prefilled from session
    initial_date = request.session.get("last_price_date") or now().date().isoformat()
    form = IngredientPriceForm(initial={"date": initial_date})

    return render(request, "manager/ingredient_price/add/index.html", {"form": form})


def get_latest_ingredient_price(request):
    name = request.GET.get("name")
    try:
        ingredient = Ingredient.objects.get(name=name)
        latest = (
            IngredientPrice.objects.filter(ingredient=ingredient)
            .order_by("-date")
            .select_related("unit", "source")
            .first()
        )
        if latest:
            return JsonResponse({
                "price": latest.price,
                "quantity": latest.quantity,
                "unit": latest.unit.name,
                "source": latest.source.name,
            })
    except Ingredient.DoesNotExist:
        pass
    return JsonResponse({}, status=404)

@staff_member_required
def diagnostics_index(request):
    summary = {}

    for category_name, module in [
        ("Recipe", diagnostics.recipe),
        ("Item", diagnostics.item),
        ("Ingredient", diagnostics.ingredient),
    ]:
        tests = module.run()
        counts = {
            test_name: len(test_data["data"]) for test_name, test_data in tests.items()
        }
        summary[category_name] = {
            "tests": counts,
            "total": sum(counts.values()),
        }

    return render(
        request,
        "manager/diagnostics/index.html",
        {
            "title": "Diagnostics Summary",
            "summary": summary,
        },
    )


@staff_member_required
def diagnostics_recipe(request):
    return render(
        request,
        "manager/diagnostics/report.html",
        {
            "title": "Recipe Diagnostics",
            "admin_change_url": "admin:manager_recipe_change",
            "diagnostics": diagnostics.recipe.run(),
        },
    )


@staff_member_required
def diagnostics_item(request):
    return render(
        request,
        "manager/diagnostics/report.html",
        {
            "title": "Item Diagnostics",
            "admin_change_url": "admin:manager_item_change",
            "diagnostics": diagnostics.item.run(),
        },
    )


@staff_member_required
def diagnostics_ingredient(request):
    return render(
        request,
        "manager/diagnostics/report.html",
        {
            "title": "Ingredient Diagnostics",
            "admin_change_url": "admin:manager_ingredient_change",
            "diagnostics": diagnostics.ingredient.run(),
        },
    )
