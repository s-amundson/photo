# Generated by Django 3.2.5 on 2022-09-18 22:52

from django.db import migrations, models
import photo_app.src.storage
import reference_images.models.reference_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('image', models.ImageField(storage=photo_app.src.storage.OverwriteStorage(), upload_to=reference_images.models.reference_model.content_file_name)),
                ('is_model_mayhem', models.BooleanField(default=False)),
                ('link', models.URLField(default=None, null=True)),
                ('note', models.CharField(max_length=255)),
                ('category', models.ManyToManyField(to='reference_images.Category')),
            ],
        ),
    ]