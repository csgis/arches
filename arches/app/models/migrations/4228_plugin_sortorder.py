# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-10-25 11:07


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "4218_plugin_permissions"),
    ]

    operations = [
        migrations.AddField(model_name="plugin", name="sortorder", field=models.IntegerField(blank=True, default=None, null=True), ),
    ]
