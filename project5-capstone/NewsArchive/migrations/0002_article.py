# Generated by Django 4.0.4 on 2022-07-06 20:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NewsArchive', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='_empty_--', max_length=20)),
                ('title', models.CharField(default='_empty_--', max_length=20)),
                ('discription', models.TextField()),
                ('article_url', models.URLField(blank=True, default='https://previews.123rf.com/images/infadel/infadel1712/infadel171200119/91684826-a-black-linear-photo-camera-logo-like-no-image-available-.jpg')),
                ('article_image_url', models.URLField(blank=True, default='https://previews.123rf.com/images/infadel/infadel1712/infadel171200119/91684826-a-black-linear-photo-camera-logo-like-no-image-available-.jpg')),
                ('publishedAt', models.DateTimeField()),
                ('source', models.CharField(default='_empty_--', max_length=30)),
                ('viewed_by', models.ManyToManyField(related_name='myNews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
