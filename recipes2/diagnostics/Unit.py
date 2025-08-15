from recipes2.models import Unit, Recipe


def run():
    return {
        "Missing Plural": {
            "template": "recipes2/diagnostics/partials/_results_table_unit_base.html",
            "data": (
                Unit.objects.filter(plural__isnull=True)
            ),
        },
    }
