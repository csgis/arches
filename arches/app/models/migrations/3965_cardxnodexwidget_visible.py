# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-29 11:09


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "3808_card_component_command"),
    ]

    operations = [
        migrations.AddField(model_name="cardxnodexwidget", name="visible", field=models.BooleanField(default=True), ),
    ]
