from manager.models import IngredientPrice, Ingredient, IngredientSource, Unit
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label="Query", max_length=100, required=False)


class IngredientPriceForm(forms.ModelForm):
    class Meta:
        model = IngredientPrice
        fields = ["date", "ingredient", "price", "quantity", "unit", "source", "detail"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create dictionary of instances by name for all the datalist fields
        self.ingredients_by_name = {obj.name: obj for obj in Ingredient.objects.all()}
        self.units_by_name = {obj.name: obj for obj in Unit.objects.all()}
        self.sources_by_name = {obj.name: obj for obj in IngredientSource.objects.all()}

        # Style the foreign key fields as text inputs with data lists, autofocus ingredient input
        self.fields["ingredient"] = forms.CharField(
            label="Ingredient",
            widget=forms.TextInput(
                attrs={
                    "list": "ingredient-list",
                    "autofocus": "autofocus",
                }
            ),
        )
        self.fields["unit"] = forms.CharField(
            label="Unit", widget=forms.TextInput(attrs={"list": "unit-list"})
        )
        self.fields["source"] = forms.CharField(
            label="Source", widget=forms.TextInput(attrs={"list": "source-list"})
        )

    def clean_ingredient(self):
        name = self.cleaned_data.get("ingredient")
        object = self.ingredients_by_name.get(name)
        if not object:
            raise forms.ValidationError(f"No ingredient named '{name}' found.")
        return object

    def clean_unit(self):
        name = self.cleaned_data.get("unit")
        object = self.units_by_name.get(name)
        if not object:
            raise forms.ValidationError(f"No unit named '{name}' found.")
        return object

    def clean_source(self):
        name = self.cleaned_data.get("source")
        object = self.sources_by_name.get(name)
        if not object:
            raise forms.ValidationError(f"No source named '{name}' found.")
        return object
