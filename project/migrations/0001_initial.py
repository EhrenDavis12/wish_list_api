# Generated by Django 3.2.5 on 2021-07-19 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pendulum
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=pendulum.now, editable=False)),
                ('last_updated', models.DateTimeField(default=pendulum.now)),
                ('name', models.CharField(default='Unknown', max_length=256)),
                ('public_note', models.CharField(blank=True, max_length=256, null=True)),
                ('private_note', models.CharField(blank=True, max_length=256, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
                'abstract': False,
            },
        ),
    ]