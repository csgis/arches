# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-26 13:06


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "deserialize_provisional_edits"),
    ]

    operations = [
        migrations.AddField(model_name="editlog", name="provisional_edittype", field=models.TextField(blank=True, null=True), ),
        migrations.AddField(model_name="editlog", name="provisional_user_username", field=models.TextField(blank=True, null=True), ),
        migrations.AddField(model_name="editlog", name="provisional_userid", field=models.TextField(blank=True, null=True), ),
    ]
