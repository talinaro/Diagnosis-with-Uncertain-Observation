import glob

from django.db import migrations

from ..consts import DATA_SYSTEMS_DIR, SYS_FILE_EXTENSION, DATA_OBSERVATIONS_DIR, OBS_FILE_EXTENSION
from ..api import parse_system, parse_observations, predict_output


def load_systems_from_dir(apps, schema_editor):
    for filepath in glob.glob(pathname=fr'{DATA_SYSTEMS_DIR}/*.{SYS_FILE_EXTENSION}'):
        parse_system(filepath)


def delete_systems(apps, schema_editor):
    System = apps.get_model("circuits_parser", "System")
    System.objects.all().delete()


def load_observations_from_dir(apps, schema_editor):
    for filepath in glob.glob(pathname=fr'{DATA_OBSERVATIONS_DIR}/*.{OBS_FILE_EXTENSION}'):
        parse_observations(filepath)


def delete_observations(apps, schema_editor):
    Observation = apps.get_model("circuits_parser", "Observation")
    Observation.objects.all().delete()


def save_all_observations_predictions(apps, schema_editor):
    Observation = apps.get_model("circuits_parser", "Observation")
    for observation in Observation.objects.all():
        predict_output(observation)


def delete_predictions(apps, schema_editor):
    Prediction = apps.get_model("circuits_parser", "Prediction")
    Prediction.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('circuits_parser', '0002_create_possible_operators'),
    ]

    operations = [
        migrations.RunPython(load_systems_from_dir, delete_systems),
        migrations.RunPython(load_observations_from_dir, delete_observations),
    ]
