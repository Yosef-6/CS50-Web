# Generated by Django 4.0.4 on 2022-07-08 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsArchive', '0004_rename_viewed_by_article_viewers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publishedAt',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
