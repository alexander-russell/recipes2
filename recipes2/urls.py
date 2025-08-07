from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from . import views

app_name = "manager"
urlpatterns = [
    path("", views.home, name="home"),
    path("csrf/", views.get_csrf_token, name="get_csrf_token"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="admin/login.html"), name="login"),
    path("accounts/login/success/", views.accounts_login_success, name="accounts_login_success"),
    path("quick-search/", views.quick_search, name="quick_search"),
    path("q/", RedirectView.as_view(pattern_name='recipes2:quick_search', permanent=False)),
    path("index/", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),
    path("explore/", views.explore, name="explore"),
    path("contents/", views.contents, name="contents"),
    path("ingredient-price/add/", views.add_ingredient_price, name="add_ingredient_price"),
    path("api/latest-ingredient/", views.get_latest_ingredient_price, name="latest-ingredient"),
    path("diagnostics/", views.diagnostics_index, name="diagnostics_index"),
    path("diagnostics/recipe/", views.diagnostics_recipe, name="diagnostics_recipe"),
    path("diagnostics/item/", views.diagnostics_item, name="diagnostics_item"),
    path("diagnostics/ingredient/", views.diagnostics_ingredient, name="diagnostics_ingredient"),
    path("<slug:recipe_slug>/", views.viewer, name="viewer"),
    path("<slug:recipe_slug>/diary/add/", views.add_diary_entry, name="add_diary_entry"),
]
