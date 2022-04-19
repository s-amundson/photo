# Generated by Django 3.2.5 on 2022-03-30 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0004_alter_gallery_display_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='pdf',
            field=models.FileField(default=None, null=True, upload_to='release/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='release',
            name='photographer_signature_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='talent_signature_date',
            field=models.DateField(default=None, null=True),
        ),
    ]