# Generated by Django 4.0.4 on 2022-07-10 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsArchive', '0018_rename_publishedstr_article_aggregateddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='aggregatedYear',
            field=models.CharField(max_length=20, null=True),
        ),
    ]