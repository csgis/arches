# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-02 18:56


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "3454_graph_node_sort_order"),
    ]

    operations = [
        migrations.RemoveField(model_name="form", name="graph", ),
        migrations.RemoveField(model_name="formxcard", name="card", ),
        migrations.RemoveField(model_name="formxcard", name="form", ),
        migrations.RemoveField(model_name="report", name="formsconfig", ),
        migrations.AlterField(model_name="node", name="sortorder", field=models.IntegerField(blank=True, default=0, null=True), ),
        migrations.DeleteModel(name="Form", ),
        migrations.DeleteModel(name="FormXCard", ),
    ]
