# Generated by Django 3.2.5 on 2022-04-15 03:23

from django.db import migrations, models
import photo_app.models.image_model


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0005_auto_20220330_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='raw_image',
            field=models.FileField(default=None, null=True, upload_to=photo_app.models.image_model.content_file_name),
        ),
    ]