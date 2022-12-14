# Generated by Django 4.0.4 on 2022-07-05 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('option', models.CharField(choices=[('Everything', 'Everything'), ('Topheadlines', 'Topheadlines')], default='Everything', max_length=15)),
                ('queryString', models.CharField(blank=True, default='_empty_--', max_length=20)),
                ('searchIn', models.CharField(blank=True, default='_empty_--', max_length=20)),
                ('sources', models.CharField(blank=True, default='_empty_--', max_length=30)),
                ('language', models.CharField(blank=True, default='en', max_length=2)),
                ('catagory', models.CharField(blank=True, default='_empty_--', max_length=30)),
                ('country', models.CharField(blank=True, default='_empty_--', max_length=20)),
                ('active', models.BooleanField()),
                ('config', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Settings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
