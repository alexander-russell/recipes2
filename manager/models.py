from decimal import Decimal
import os
from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError
from django.utils.text import slugify
from django.utils import timezone


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Classification(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("type", "category")

    def __str__(self):
        return ", ".join([self.type.name, self.category.name])


class YieldUnit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    plural = models.CharField(max_length=50)
    singular = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    def label(self, quantity):
        return (
            self.singular
            if self.singular is not None and quantity == 1
            else self.plural
        )


class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Recipe.Status.ACTIVE)


class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Recipe(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"  # For unfinished recipes
        ACTIVE = "active", "Active"  # For most recipes
        HIDDEN = "hidden", "Hidden"  # Unused as yet
        ARCHIVED = "archived", "Archived"  # For formerly 'retired' recipes

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    classification = models.ForeignKey(
        Classification, on_delete=models.CASCADE, related_name="recipes"
    )
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    needs_revision = models.BooleanField()
    yield_quantity = models.SmallIntegerField(blank=True, null=True)
    yield_unit = models.ForeignKey(
        YieldUnit, blank=True, null=True, on_delete=models.CASCADE
    )
    yield_detail = models.CharField(max_length=200, blank=True, null=True)
    time_quantity = models.DurationField(blank=True, null=True)
    time_detail = models.CharField(max_length=200, blank=True, null=True)
    difficulty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True
    )
    bulk = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)
    tested = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)
    cuisine = models.ForeignKey(
        Cuisine,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="recipes",
    )
    description = models.TextField()

    # Use custom manager (gives me access to custom queryset)
    objects = RecipeManager()

    # def save(self, *args, **kwargs):
    #     if not self.pk or Recipe.objects.get(pk=self.pk).name != self.name:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def update_cost(self) -> "RecipeCost":
        # Get or create associated RecipeCost
        try:
            recipe_cost = self.cost
        except RecipeCost.DoesNotExist:
            recipe_cost = RecipeCost(recipe=self)

        # Calculate total
        total = Decimal("0.00")
        full_success = True
        for item in self.items.all():
            item_cost = item.get_cost()
            full_success &= item_cost.success
            if item_cost.amount is not None:
                total += item_cost.amount

        # Populate model fields and save
        recipe_cost.recipe = self
        recipe_cost.total = total
        if (
            self.yield_unit is not None
            and self.yield_quantity is not None
            and self.yield_quantity is not 0
        ):  # TODO this last check shouldn't be necessary with proper data import
            recipe_cost.amount_per_unit = total / self.yield_quantity
            recipe_cost.yield_unit = self.yield_unit
        recipe_cost.full_success = full_success
        recipe_cost.save()
        return recipe_cost

    def get_cost(self) -> "RecipeCost":
        try:
            return self.cost
        except:
            return self.update_cost()


class RecipeCost(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name="cost")
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_per_unit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    yield_unit = models.ForeignKey(YieldUnit, on_delete=models.SET_NULL, null=True)
    full_success = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_latest_price(self):
        return self.prices.order_by("-date").first()


class Unit(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Conversion(models.Model):
    from_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="conversions_from"
    )
    to_unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="conversions_to"
    )
    factor = models.DecimalField(
        max_digits=7, decimal_places=3, validators=[MinValueValidator(0)]
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.from_unit.name}->{self.to_unit.name}{' (' + self.ingredient.name + ')' if self.ingredient else ''}"


class IngredientSource(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class IngredientPrice(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="prices"
    )
    date = models.DateField(default=timezone.now)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.DecimalField(max_digits=7, decimal_places=3)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    source = models.ForeignKey(IngredientSource, on_delete=models.CASCADE)
    detail = models.CharField(max_length=200, null=True, blank=True)


class ItemGroup(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="items")
    position = models.PositiveIntegerField(default=0, db_index=True)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="items"
    )
    ingredient_detail = models.CharField(max_length=100, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="items")
    unit_detail = models.CharField(max_length=100, blank=True)
    group = models.ForeignKey(
        ItemGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="items",
    )

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.ingredient.name

    def update_cost(self) -> "ItemCost":
        # Get or create item cost instance for this item
        try:
            item_cost = self.cost
        except ItemCost.DoesNotExist:
            item_cost = ItemCost(item=self)

        # Set starting values
        item_cost.success = False
        item_cost.reason = None
        item_cost.amount = None
        item_cost.ingredient_name = self.ingredient.name
        item_cost.item_quantity = self.quantity
        item_cost.item_unit = self.unit
        item_cost.price = None
        item_cost.price_quantity = None
        item_cost.price_unit = None

        # If quantity is zero, stop. Otherwise get price
        if self.quantity == 0:
            item_cost.reason = "zeroquantity"
            item_cost.save()
            return item_cost
        else:
            latest_price = self.ingredient.get_latest_price()

            # Stop if no price or price is zero, otherwise calculate conversion factor
            if not latest_price:
                item_cost.reason = "noprice"
                item_cost.save()
                return item_cost
            elif latest_price.price == 0:
                item_cost.reason = "latestpriceiszero"
                item_cost.save()
                return item_cost
            else:
                # Fill out price details
                item_cost.price = latest_price.price
                item_cost.price_quantity = latest_price.quantity
                item_cost.price_unit = (
                    latest_price.unit.name if latest_price.unit else None
                )

                # If units are the same use 1, otherwise calculate it with unit graph
                if self.unit.name == latest_price.unit.name:
                    conversion_factor = 1
                else:
                    from manager.utils.cost_utils2 import get_conversion_factor

                    conversion_factor = get_conversion_factor(
                        self.unit.name, latest_price.unit.name, self.ingredient.id
                    )
                # If conversion failed, stop, otherwise calculate amount and return
                if conversion_factor is None:
                    item_cost.reason = "noconversion"
                    item_cost.save()
                    return item_cost
                else:
                    item_cost.success = True
                    item_cost.amount = (
                        self.quantity
                        / latest_price.quantity
                        * latest_price.price
                        * conversion_factor
                    )
                    item_cost.save()
                    return item_cost

    def get_cost(self) -> "ItemCost":
        try:
            return self.cost
        except:
            return self.update_cost()


class ItemCost(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name="cost")
    success = models.BooleanField(default=False)
    reason = models.TextField(null=True, blank=True)
    ingredient_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    item_unit = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    price_unit = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class StepGroup(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")
    position = models.PositiveIntegerField()
    content = models.TextField()
    group = models.ForeignKey(
        StepGroup, on_delete=models.CASCADE, blank=True, null=True
    )


class Diary(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="diaryentries"
    )
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()


class Timer(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="timers")
    position = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    duration = models.DurationField()


def image_upload_to(instance, filename):
    return os.path.join("manager", str(instance.recipe.id), "images", filename)

def validate_avif_extension(value):
    extension = os.path.splitext(value.name)[1].lower()
    if extension not in ['.avif']:
        raise ValidationError('Must be an AVIF image.')


class Image(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="images")
    position = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    alt_text = models.CharField(max_length=200, null=True)
    show_in_gallery = models.BooleanField()
    image = models.FileField(upload_to=image_upload_to, validators=[validate_avif_extension])

    class Meta:
        unique_together = ("recipe", "name")

    # def clean(self):
    #     if False and not self.image.name.lower().endswith(".avif"):
    #         raise ValidationError("Only AVIF images are allowed.")

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)


class Tag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=100)
