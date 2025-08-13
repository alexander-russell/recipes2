from recipes2.models import Step, Recipe
from django.db.models import F

def run():
    return {
        "Group Recipe Mismatch": {
            "template": "recipes2/diagnostics/partials/_results_table_step_group.html",
            "data": (
                Step.objects.filter(recipe__status=Recipe.Status.ACTIVE)
                .exclude(group__isnull=True)
                .exclude(recipe__id=F('group__recipe__id'))
            ),
        },
    }
