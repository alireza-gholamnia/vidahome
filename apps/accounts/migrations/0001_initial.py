# Migration for custom User model (replaces UserProfile)

import apps.common.upload_utils
import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "__latest__"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False)),
                ("username", models.CharField(error_messages={"unique": "A user with that username already exists."}, max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("avatar", models.ImageField(blank=True, null=True, upload_to=apps.common.upload_utils.avatar_upload_to)),
                ("is_verified", models.BooleanField(default=False)),
                ("groups", models.ManyToManyField(blank=True, related_name="user_set", to="auth.group")),
                ("user_permissions", models.ManyToManyField(blank=True, related_name="user_set", to="auth.permission")),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
