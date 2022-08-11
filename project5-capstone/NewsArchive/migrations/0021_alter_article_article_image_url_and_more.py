# Generated by Django 4.0.4 on 2022-07-10 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsArchive', '0020_alter_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_image_url',
            field=models.URLField(blank=True, default='https://previews.123rf.com/images/infadel/infadel1712/infadel171200119/91684826-a-black-linear-photo-camera-logo-like-no-image-available-.jpg', max_length=450),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_url',
            field=models.URLField(blank=True, default='https://previews.123rf.com/images/infadel/infadel1712/infadel171200119/91684826-a-black-linear-photo-camera-logo-like-no-image-available-.jpg', max_length=450),
        ),
    ]