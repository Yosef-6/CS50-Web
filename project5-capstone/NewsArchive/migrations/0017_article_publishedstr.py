# Generated by Django 4.0.4 on 2022-07-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsArchive', '0016_alter_configuration_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publishedStr',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
