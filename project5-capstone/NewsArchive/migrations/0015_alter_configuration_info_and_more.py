# Generated by Django 4.0.4 on 2022-07-09 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsArchive', '0014_alter_article_viewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='info',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='language',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
