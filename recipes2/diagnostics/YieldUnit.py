from django.db.models import Q
from recipes2.models import YieldUnit, Recipe


def run():
    return {
        "Missing Plural": {
            "template": "recipes2/diagnostics/partials/_results_table_unit_base.html",
            "data": (YieldUnit.objects.filter(Q(plural__isnull=True) | Q(plural=""))),
        },
    }
