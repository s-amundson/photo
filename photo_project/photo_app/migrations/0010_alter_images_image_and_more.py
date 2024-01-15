# Generated by Django 4.2.6 on 2024-01-13 19:26

from django.db import migrations, models
import photo_app.models.image_model
import photo_app.src.storage


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0009_imagecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(storage=photo_app.src.storage.OverwriteStorage(), upload_to=photo_app.models.image_model.content_file_name),
        ),
        migrations.AlterField(
            model_name='release',
            name='photographer_signature',
            field=models.ImageField(default=None, null=True, storage=photo_app.src.storage.OverwriteStorage(), upload_to='signatures/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='release',
            name='talent_signature',
            field=models.ImageField(default=None, null=True, storage=photo_app.src.storage.OverwriteStorage(), upload_to='signatures/%Y/%m/%d/'),
        ),
    ]