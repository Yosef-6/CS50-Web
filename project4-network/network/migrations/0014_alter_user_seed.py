# Generated by Django 4.0.4 on 2022-06-19 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_alter_user_seed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='seed',
            field=models.CharField(default='q7rGdrp9QT', max_length=10),
        ),
    ]