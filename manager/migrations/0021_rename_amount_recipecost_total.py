# Generated by Django 5.2.3 on 2025-07-22 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0020_recipecost_recipe"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recipecost",
            old_name="amount",
            new_name="total",
        ),
    ]
