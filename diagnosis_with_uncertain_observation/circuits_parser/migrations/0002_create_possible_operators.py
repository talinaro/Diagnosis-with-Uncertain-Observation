from django.db import migrations

from ..models.operators import operators


def load_operator_types(apps, schema_editor):
    OperatorType = apps.get_model("circuits_parser", "OperatorType")
    for op_name in operators.keys():
        OperatorType.objects.create(name=op_name)


def delete_operator_types(apps, schema_editor):
    OperatorType = apps.get_model("circuits_parser", "OperatorType")
    OperatorType.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('circuits_parser', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_operator_types, delete_operator_types),
    ]
