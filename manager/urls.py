from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from . import views

app_name = "manager"
urlpatterns = [
    path("", views.home, name="home"),
    path("quick-search", views.quick_search, name="quick_search"),
    path("q", RedirectView.as_view(pattern_name='manager:quick_search', permanent=False)),
    path("index", views.index, name="index"),
    path("gallery", views.gallery, name="gallery"),
    path("explore", views.explore, name="explore"),
    path("contents", views.contents, name="contents"),
    path("diagnostics", views.diagnostics_index_view, name="diagnostics_index"),
    path("diagnostics/recipes", views.diagnostics_recipes_view, name="diagnostics_recipes"),
    path("diagnostics/items", views.diagnostics_items_view, name="diagnostics_items"),
    path("diagnostics/ingredients", views.diagnostics_ingredients_view, name="diagnostics_ingredients"),
    path("<slug:recipe_slug>", views.viewer, name="viewer"),
    path("<slug:recipe_slug>/diary/add", views.add_diary_entry, name="add_diary_entry"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
