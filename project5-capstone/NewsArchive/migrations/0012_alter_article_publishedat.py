# Generated by Django 4.0.4 on 2022-07-09 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsArchive', '0011_remove_article_viewers_article_viewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publishedAt',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
