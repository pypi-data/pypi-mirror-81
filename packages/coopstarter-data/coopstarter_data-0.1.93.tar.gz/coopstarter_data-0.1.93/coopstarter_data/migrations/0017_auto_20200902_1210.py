# Generated by Django 2.2 on 2020-09-02 12:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djangoldp.fields


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coopstarter_data', '0016_auto_20200824_1509'),
    ]

    operations = [
        migrations.RenameModel('Mentor', 'Contributor'),
        migrations.RenameModel('Entrepreneur', 'Searcher')
    ]
