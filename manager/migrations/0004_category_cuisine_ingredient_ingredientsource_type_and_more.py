# Generated by Django 5.2.3 on 2025-06-29 07:45

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0003_remove_recipe_desc"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Cuisine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="IngredientSource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Type",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Unit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="YieldUnit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("plural", models.CharField(max_length=50)),
                ("singular", models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="pub_date",
        ),
        migrations.AddField(
            model_name="recipe",
            name="bulk",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="recipe",
            name="date_created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="recipe",
            name="date_updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="description",
            field=models.TextField(default="description"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="difficulty",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(10),
                ],
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="favourite",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="recipe",
            name="gluten_free",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="recipe",
            name="needs_revision",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="slug",
            field=models.CharField(default="a", max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("active", "Active"),
                    ("hidden", "Hidden"),
                    ("archived", "Archived"),
                ],
                default="draft",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tested",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="recipe",
            name="time_detail",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="recipe",
            name="time_quantity",
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="recipe",
            name="vegan",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="recipe",
            name="vegetarian",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="recipe",
            name="yield_detail",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="recipe",
            name="yield_quantity",
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.CreateModel(
            name="Classification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.category",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="manager.type"
                    ),
                ),
            ],
            options={
                "unique_together": {("type", "category")},
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="classification",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipes",
                to="manager.classification",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="cuisine",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="manager.cuisine",
            ),
        ),
        migrations.CreateModel(
            name="Diary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("content", models.TextField()),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="diaryentries",
                        to="manager.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ItemGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="manager.recipe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Step",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.PositiveIntegerField()),
                ("content", models.TextField()),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.itemgroup",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="steps",
                        to="manager.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StepGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="manager.recipe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tags",
                        to="manager.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Timer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=100)),
                ("duration", models.DurationField(blank=True)),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="timers",
                        to="manager.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.PositiveIntegerField()),
                ("ingredient_detail", models.CharField(blank=True, max_length=100)),
                ("quantity", models.DecimalField(decimal_places=3, max_digits=10)),
                ("unit_detail", models.CharField(blank=True, max_length=100)),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.ingredient",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="manager.recipe",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.itemgroup",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="manager.unit"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IngredientPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("quantity", models.DecimalField(decimal_places=3, max_digits=5)),
                ("detail", models.CharField(max_length=200)),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices",
                        to="manager.ingredient",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.ingredientsource",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="manager.unit"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UnitConversion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "factor",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "from_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="from_unit",
                        to="manager.unit",
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.ingredient",
                    ),
                ),
                (
                    "to_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to_unit",
                        to="manager.unit",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="recipe",
            name="yield_unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="manager.yieldunit",
            ),
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="")),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="manager.recipe",
                    ),
                ),
            ],
            options={
                "unique_together": {("recipe", "name")},
            },
        ),
    ]
