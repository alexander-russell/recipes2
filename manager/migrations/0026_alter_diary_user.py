# Generated by Django 5.2.3 on 2025-07-27 07:19
# With modification by Alex when it didn't work because "foo" wasn't a valid default for the field user

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.contrib.auth import get_user_model

# User = get_user_model()
# admin_user = User.objects.get(username="admin")

def set_diary_user_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Diary = apps.get_model('manager', 'Diary')
    try:
        admin_user = User.objects.get(username='admin')
        Diary.objects.filter(user__isnull=True).update(user=admin_user)
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0025_diary_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(set_diary_user_admin),
        # migrations.AlterField(
        #     model_name="diary",
        #     name="user",
        #     field=models.ForeignKey(
        #         default=admin_user.id,
        #         on_delete=django.db.models.deletion.PROTECT,
        #         to=settings.AUTH_USER_MODEL,
        #     ),
        #     preserve_default=False,
        # ),
    ]
