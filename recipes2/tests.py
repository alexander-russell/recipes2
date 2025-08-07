from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from recipes2.models import (
    Type, Category, Classification,
    YieldUnit, Cuisine, Recipe
)

class ViewTests(TestCase):
    def setUp(self):
        # Required related objects
        self.type = Type.objects.create(name="Main")
        self.category = Category.objects.create(name="Dinner")
        self.classification = Classification.objects.create(
            type=self.type, category=self.category
        )
        self.yield_unit = YieldUnit.objects.create(
            name="serving", plural="servings", singular="serving"
        )
        self.cuisine = Cuisine.objects.create(name="Italian")

        # Create a test recipe
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            slug="test-recipe",
            classification=self.classification,
            date_created=timezone.now().date(),
            date_updated=timezone.now().date(),
            status=Recipe.Status.ACTIVE,
            needs_revision=False,
            yield_quantity=4,
            yield_unit=self.yield_unit,
            yield_detail="medium tray",
            time_quantity=None,
            time_detail="About 1 hour",
            difficulty=5,
            bulk=False,
            favourite=True,
            tested=True,
            vegetarian=True,
            vegan=False,
            gluten_free=False,
            cuisine=self.cuisine,
            description="Test recipe description"
        )

    def test_explore_view(self):
        response = self.client.get(reverse("recipes2:explore"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes2/explore/index.html")
        self.assertContains(response, self.recipe.name)

    def test_home_view(self):
        response = self.client.get(reverse("recipes2:home"))
        self.assertEqual(response.status_code, 200)

    def test_index_view(self):
        response = self.client.get(reverse("recipes2:index"))
        self.assertEqual(response.status_code, 200)

    def test_contents_view(self):
        response = self.client.get(reverse("recipes2:contents"))
        self.assertEqual(response.status_code, 200)

    def test_gallery_view(self):
        response = self.client.get(reverse("recipes2:gallery"))
        self.assertEqual(response.status_code, 200)

    def test_viewer_view(self):
        response = self.client.get(reverse("recipes2:viewer", args=[self.recipe.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.name)
