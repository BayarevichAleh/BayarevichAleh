# Generated by Django 3.1 on 2020-10-05 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0003_auto_20201005_2022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='forum',
            new_name='id_forum',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='id_user',
        ),
    ]
