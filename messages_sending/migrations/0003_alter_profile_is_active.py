# Generated by Django 4.1.1 on 2022-09-07 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_sending', '0002_message_message_messages_se_receive_63f455_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]