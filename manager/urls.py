from django.urls import path

from . import views

app_name = "manager"
urlpatterns = [
    # ex: /manager/
    path("", views.index, name="index"),
    path("contents", views.contents, name="contents"),
    # ex: /manager/5/
    path("<slug:recipe_slug>/", views.view, name="view"),
    # # ex: /polls/5/results/
    # path("<int:question_id>/results/", views.results, name="results"),
    # # ex: /polls/5/vote/
]
