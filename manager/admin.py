from django import forms
from django.contrib import admin
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
    Timer,
    Type,
    Unit,
    YieldUnit,
)
from adminsortable2.admin import (
    SortableInlineAdminMixin,
    SortableTabularInline,
    SortableAdminBase,
    SortableAdminMixin,
)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    search_fields = ["category__name"]


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(YieldUnit)
class YieldUnitAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class ItemInline(admin.TabularInline):
    autocomplete_fields = ["ingredient", "unit"]
    model = Item
    extra = 0


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(IngredientSource)
class IngredientSourceAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["name"]


@admin.register(IngredientPrice)
class IngredientPriceAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'date', 'source', 'price', 'quantity', 'unit', 'detail'] 
    ordering = ["-date"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]



@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    pass


class StepInline(admin.TabularInline):
    model = Step
    extra = 0


@admin.register(StepGroup)
class StepGroupAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class TimerInline(admin.TabularInline):
    model = Timer
    extra = 0


class DiaryInline(admin.TabularInline):
    model = Diary
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # pass
    autocomplete_fields = ["cuisine", "classification", "yield_unit"]
    # readonly_fields = ("slug",)
    prepopulated_fields = {'slug': ('name',)}
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
        js = ('admin/recipe.js',)


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ['from_unit', 'factor', 'to_unit', 'ingredient'] 
    ordering = ['ingredient', 'from_unit', 'to_unit']