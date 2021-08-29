from django.db import migrations
from django.core.management import call_command


def forwards_func(apps, schema_editor):
    print('forwards')
    call_command('loaddata', 'fixtures/project.json', verbosity=2)


def reverse_func(apps, schema_editor):
    print('reverse')


class Migration(migrations.Migration):
    dependencies = [
        ('project', '0001_initial'), ('app_user', '0002_load_fixtures')
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]