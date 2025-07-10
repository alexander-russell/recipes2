from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from manager.models import Recipe


def index(request):
    return HttpResponse(
        "Hello, world. You're at the manager index. <a href=" "contents" ">hey</a>"
    )


def contents(request):
    all_recipes = Recipe.objects.all()
    context = {"all_recipes": all_recipes}
    return render(request, "manager/contents/index.html", context)


def view(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(request, "manager/view/index.html", {"recipe": recipe})


# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
