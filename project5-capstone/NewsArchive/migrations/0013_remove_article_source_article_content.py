# Generated by Django 4.0.4 on 2022-07-09 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsArchive', '0012_alter_article_publishedat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='source',
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
