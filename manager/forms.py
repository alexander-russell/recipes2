from manager.models import IngredientPrice, Ingredient, Unit
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label="Query", max_length=100, required=False)

class IngredientPriceForm(forms.ModelForm):
    ingredient_name = forms.CharField()
    unit_name = forms.CharField()

    class Meta:
        model = IngredientPrice
        fields = ["date", "price", "quantity", "source", "detail"]

    def clean_ingredient_name(self):
        name = self.cleaned_data["ingredient_name"].strip()
        try:
            return Ingredient.objects.get(name__iexact=name)
        except Ingredient.DoesNotExist:
            raise forms.ValidationError("Unknown ingredient")

    def clean_unit_name(self):
        name = self.cleaned_data["unit_name"].strip()
        try:
            return Unit.objects.get(name__iexact=name)
        except Unit.DoesNotExist:
            raise forms.ValidationError("Unknown unit")

    def save(self, commit=True):
        self.instance.ingredient = self.cleaned_data["ingredient_name"]
        self.instance.unit = self.cleaned_data["unit_name"]
        return super().save(commit=commit)
