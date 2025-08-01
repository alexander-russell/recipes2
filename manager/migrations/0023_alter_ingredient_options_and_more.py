# Generated by Django 5.2.3 on 2025-07-25 11:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0022_recipecost_amount_per_unit_recipecost_yield_unit"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredient",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="ingredientsource",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="unit",
            options={"ordering": ["name"]},
        ),
        migrations.AlterField(
            model_name="ingredientprice",
            name="detail",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="item",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="items",
                to="manager.itemgroup",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="manager.ingredient",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="manager.unit",
            ),
        ),
    ]
