# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-21 19:18


from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("models", "4669_remove_workflow_plugin"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConstraintModel",
            fields=[
                ("constraintid", models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ("card", models.ForeignKey(db_column="cardid", on_delete=django.db.models.deletion.CASCADE, to="models.CardModel")),
            ],
            options={"db_table": "card_constraints", "managed": True, },
        ),
        migrations.CreateModel(
            name="ConstraintXNode",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                (
                    "constraint",
                    models.ForeignKey(db_column="constraintid", on_delete=django.db.models.deletion.CASCADE, to="models.ConstraintModel"),
                ),
                ("node", models.ForeignKey(db_column="nodeid", on_delete=django.db.models.deletion.CASCADE, to="models.Node")),
            ],
            options={"db_table": "constraints_x_nodes", "managed": True, },
        ),
        migrations.AddField(
            model_name="constraintmodel", name="nodes", field=models.ManyToManyField(through="models.ConstraintXNode", to="models.Node"),
        ),
        migrations.AddField(model_name="constraintmodel", name="uniquetoallinstances", field=models.BooleanField(default=False), ),
    ]
