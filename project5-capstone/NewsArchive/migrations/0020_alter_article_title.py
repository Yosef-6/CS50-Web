# Generated by Django 4.0.4 on 2022-07-10 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsArchive', '0019_article_aggregatedyear'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.TextField(),
        ),
    ]
