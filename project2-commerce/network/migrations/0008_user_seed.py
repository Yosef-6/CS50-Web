# Generated by Django 4.0.4 on 2022-06-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_remove_user_seed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='seed',
            field=models.CharField(default='%.1RK(w=sk', max_length=10),
        ),
    ]
