# Generated by Django 4.0.2 on 2022-02-05 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The product name', max_length=255)),
                ('url', models.CharField(help_text='The url to the product', max_length=1024)),
                ('phrase', models.CharField(help_text='This phrase will be searched on the website - if the phrase is not there then the item should be in stock', max_length=255)),
                ('date_added', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('found', models.BooleanField(default=False)),
                ('date_found', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
