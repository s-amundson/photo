# Generated by Django 3.2.5 on 2022-03-25 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0002_alter_gallery_display_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='display_image',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
