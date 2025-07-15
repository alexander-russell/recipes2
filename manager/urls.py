from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "manager"
urlpatterns = [
    path("", views.home, name="home"),
    path("index", views.index, name="index"),
    path("gallery", views.gallery, name="gallery"),
    path("explore", views.explore, name="explore"),
    path("contents", views.contents, name="contents"),
    path("<slug:recipe_slug>", views.viewer, name="viewer"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
