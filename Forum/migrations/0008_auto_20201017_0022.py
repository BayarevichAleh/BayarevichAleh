# Generated by Django 3.1 on 2020-10-16 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0007_auto_20201015_0948'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forum',
            old_name='is_pablished',
            new_name='is_published',
        ),
    ]
