# Generated by Django 5.1.6 on 2025-03-05 18:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("login", "0002_user_created_at_user_modified_at_profile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VehicleMaster",
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
                ("brand", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
                ("year", models.IntegerField()),
                (
                    "fuel_type",
                    models.CharField(
                        choices=[
                            ("Petrol", "Petrol"),
                            ("Diesel", "Diesel"),
                            ("Electric", "Electric"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "transmission",
                    models.CharField(
                        choices=[("Manual", "Manual"), ("Automatic", "Automatic")],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanyInventory",
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
                ("quantity", models.PositiveIntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inventory",
                        to="login.company",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="company_inventory",
                        to="inventory.vehiclemaster",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanyInventoryImage",
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
                ("image", models.ImageField(upload_to="company_inventory_images/")),
                (
                    "inventory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="inventory.companyinventory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VehicleDocument",
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
                ("document_type", models.CharField(max_length=100)),
                ("file", models.FileField(upload_to="documents/")),
                (
                    "inventory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="inventory.companyinventory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VehicleMasterImage",
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
                ("image", models.ImageField(upload_to="vehicle_master_images/")),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="inventory.vehiclemaster",
                    ),
                ),
            ],
        ),
    ]
