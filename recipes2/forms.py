from recipes2.models import (
    Category,
    Cuisine,
    IngredientPrice,
    Ingredient,
    IngredientSource,
    Type,
    Unit,
)
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label="Query", max_length=100, required=False)
    SEARCH_SCOPE_CHOICES = [
        ("title", "title"),
        ("everywhere", "everywhere"),
    ]
    search_scope = forms.ChoiceField(
        label="in",
        choices=SEARCH_SCOPE_CHOICES,
        initial="title",
        widget=forms.Select,
        required=True,
    )

    type = forms.ModelChoiceField(
        label="Type", queryset=Type.objects.all(), required=False, empty_label="Any"
    )
    category = forms.ModelChoiceField(
        label="Category",
        queryset=Category.objects.all(),
        required=False,
        empty_label="Any",
    )
    vegetarian = forms.BooleanField(label="Vegetarian", required=False)
    vegan = forms.BooleanField(label="Vegan", required=False)
    gluten_free = forms.BooleanField(label="Gluten Free", required=False)
    cuisine = forms.ModelChoiceField(
        label="Cuisine",
        queryset=Cuisine.objects.all(),
        required=False,
        empty_label="Any",
    )
    # Add sorting choice
    SORT_CHOICES = [
        ("name", "Name"),
        ("time_quantity", "Time"),
        ("difficulty", "Difficulty"),
        ("cost", "Cost"),
        ("cost_per_serve", "Cost per serve"),
        ("random", "Random"),
    ]
    sort = forms.ChoiceField(
        label="Sort by",
        choices=SORT_CHOICES,
        initial="name",
        required=False,
    )

    SORT_DIRECTION_CHOICES = [
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
    ]
    sort_direction = forms.ChoiceField(
        label="Sort direction",
        choices=SORT_DIRECTION_CHOICES,
        initial='asc',
        required=False,
    )


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
