# Generated by Django 4.1.3 on 2022-11-21 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budgetApp", "0002_sharedexpense_expensecategory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="BirthDate",
            field=models.DateField(default="2022-11-21"),
        ),
    ]
