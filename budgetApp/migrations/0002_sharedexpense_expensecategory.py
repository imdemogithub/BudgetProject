# Generated by Django 4.1.3 on 2022-11-21 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("budgetApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sharedexpense",
            name="ExpenseCategory",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="budgetApp.expensecategory",
            ),
            preserve_default=False,
        ),
    ]
