# serializers.py
from rest_framework import serializers
from .models import IngredientPrice

class IngredientPriceSerializer(serializers.ModelSerializer):
    ingredient = serializers.CharField(source="ingredient.name")
    unit = serializers.CharField(source="unit.singular")
    source = serializers.CharField(source="source.name")
    price = serializers.FloatField()
    quantity = serializers.FloatField()

    class Meta:
        model = IngredientPrice
        fields = ["ingredient", "price", "quantity", "unit", "source", "date"]
