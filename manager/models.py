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
        Cuisine, on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk or Recipe.objects.get(pk=self.pk).name != self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_latest_price(self):
        return self.prices.order_by("-date").first()


class Unit(models.Model):
    name = models.CharField(max_length=100)

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
    detail = models.CharField(max_length=200)


class ItemGroup(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="items")
    position = models.PositiveIntegerField(default=0, db_index=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    ingredient_detail = models.CharField(max_length=100, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    unit_detail = models.CharField(max_length=100, blank=True)
    group = models.ForeignKey(
        ItemGroup, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.ingredient.name

    def get_cost(self):
        from manager.utils.cost_utils2 import get_conversion_factor

        result = {
            "amount": None,
            "success": False,
            "reason": None,
            "price": None,
            "ingredientname": self.ingredient.name,
            "itemquantity": self.quantity,
            "pricequantity": None,
            "itemunit": self.unit,
            "priceunit": None,
        }

        if self.quantity == 0:
            result["reason"] = "zeroquantity"
            return result

        latest_price = self.ingredient.get_latest_price()

        if not latest_price:
            result["reason"] = "noprice"
            return result

        if latest_price.price == 0:
            result["reason"] = "latestpriceiszero"
            return result

        if self.unit.name == latest_price.unit.name:
            conversion_factor = 1
        else:
            conversion_factor = get_conversion_factor(
                self.unit.name, latest_price.unit.name, self.ingredient.id
            )

            if conversion_factor is None:
                result["reason"] = "noconversion"
                return result

        # Step 3: Calculate the cost
        amount = (
            self.quantity
            / latest_price.quantity
            * latest_price.price
            * conversion_factor
        )

        result["amount"] = amount
        result["success"] = True
        result["price"] = latest_price.price
        result["priceunit"] = latest_price.unit
        result["pricequantity"] = latest_price.quantity
        result["unit"] = latest_price.unit
        return result


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


class Image(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="images")
    position = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    image = models.ImageField()

    class Meta:
        unique_together = ("recipe", "name")

    def clean(self):
        if False and not self.image.name.lower().endswith(".avif"):
            raise ValidationError("Only AVIF images are allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Tag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=100)
