from django import forms
from django.contrib import admin
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import (
    Category,
    Classification,
    Conversion,
    Cuisine,
    Diary,
    Image,
    Ingredient,
    IngredientPrice,
    IngredientSource,
    Item,
    ItemGroup,
    Recipe,
    Step,
    StepGroup,
    Tag,
    Timer,
    Type,
    Unit,
    YieldUnit,
)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    search_fields = ["type__name", "category__name"]


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(YieldUnit)
class YieldUnitAdmin(admin.ModelAdmin):
    search_fields = ["singular"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("recipe__name", "ingredient__name", "quantity", "unit__singular", "group__name")
    list_display_links = ("ingredient__name",)
    search_fields = ("recipe__name", "ingredient__name", "unit__singular", "group__name")


class ItemInline(SortableInlineAdminMixin, admin.TabularInline):
    autocomplete_fields = ["ingredient", "unit"]
    model = Item
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            recipe_id = request.resolver_match.kwargs.get("object_id")
            if recipe_id:
                kwargs["queryset"] = ItemGroup.objects.filter(recipe_id=recipe_id)
            else:
                kwargs["queryset"] = ItemGroup.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(IngredientSource)
class IngredientSourceAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["name"]


@admin.register(IngredientPrice)
class IngredientPriceAdmin(admin.ModelAdmin):
    list_display = [
        "ingredient",
        "date",
        "source",
        "price",
        "quantity",
        "unit",
        "detail",
    ]
    ordering = ["-date"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ["singular"]
    ordering = ["singular"]


@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        data = super().get_changeform_initial_data(request)
        recipe_id = request.GET.get("recipe")
        if recipe_id:
            data["recipe"] = recipe_id
        return data

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.GET.get("recipe") and "recipe" in form.base_fields:
            form.base_fields["recipe"].disabled = True
        return form


class StepInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Step
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            recipe_id = request.resolver_match.kwargs.get("object_id")
            if recipe_id:
                kwargs["queryset"] = StepGroup.objects.filter(recipe_id=recipe_id)
            else:
                kwargs["queryset"] = StepGroup.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(StepGroup)
class StepGroupAdmin(admin.ModelAdmin): 
    def get_changeform_initial_data(self, request):
        data = super().get_changeform_initial_data(request)
        recipe_id = request.GET.get("recipe")
        if recipe_id:
            data["recipe"] = recipe_id
        return data

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.GET.get("recipe") and "recipe" in form.base_fields:
            form.base_fields["recipe"].disabled = True
        return form


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 0


class TimerInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Timer
    extra = 0


class DiaryInline(admin.TabularInline):
    model = Diary
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Set the default for the `user` field to the logged-in user
        formset.form.base_fields["user"].initial = request.user
        return formset


class TagInline(admin.TabularInline):
    model = Tag
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(SortableAdminBase, admin.ModelAdmin):
    # pass
    autocomplete_fields = ["cuisine", "classification", "yield_unit"]
    # readonly_fields = ("slug",)
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ItemInline, StepInline, ImageInline, TimerInline, DiaryInline, TagInline]
    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["name", "slug", "classification", "description"],
                "classes": [],
            },
        ),
        (
            "Status",
            {"fields": ["date_created", "date_updated", "status"], "classes": []},
        ),
        (
            "Details",
            {
                "fields": [
                    ("yield_quantity", "yield_detail", "yield_unit"),
                    ("time_quantity", "time_detail"),
                    "difficulty",
                    "cuisine",
                ],
                "classes": [],
            },
        ),
        (
            "Attributes",
            {
                "fields": [
                    "bulk",
                    "favourite",
                    "tested",
                    "needs_revision",
                    "vegetarian",
                    "vegan",
                    "gluten_free",
                ],
                "classes": [],
            },
        ),
    ]

    class Media:
        css = {"all": ("admin/recipe.css",)}
        js = ("admin/recipe.js",)

@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ["from_unit", "factor", "to_unit", "ingredient"]
    ordering = ["ingredient", "from_unit", "to_unit"]

# class UserAdmin(admin.ModelAdmin):

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ("date", "user", "recipe", "content")
    list_filter = ("user", "date", "recipe")
    search_fields = ("content", "recipe__name", "user__username")
    date_hierarchy = "date"