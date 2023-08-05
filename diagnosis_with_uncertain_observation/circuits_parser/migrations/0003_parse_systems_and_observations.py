import glob

from django.db import migrations

from ..consts import SYS_FILE_EXTENSION, OBS_FILE_EXTENSION
from diagnosis_with_uncertain_observation.circuits_parser.config import DATA_SYSTEMS_DIR, DATA_OBSERVATIONS_DIR
from ..api import parse_system, parse_observations


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


class Migration(migrations.Migration):

    dependencies = [
        ('circuits_parser', '0002_create_possible_operators'),
    ]

    operations = [
        migrations.RunPython(load_systems_from_dir, delete_systems),
        migrations.RunPython(load_observations_from_dir, delete_observations),
    ]
