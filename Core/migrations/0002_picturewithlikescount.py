# Generated by Django 2.0.5 on 2018-05-27 21:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PictureWithLikesCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='media_dir/%Y/%m/%d/%S')),
                ('description', models.CharField(blank=True, max_length=50)),
                ('key', models.SlugField(max_length=4, unique=True)),
                ('uploadTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastViewTime', models.DateTimeField(null=True)),
                ('viewCounter', models.PositiveIntegerField(default=0)),
                ('like_count', models.IntegerField()),
                ('dislike_count', models.IntegerField()),
                ('likes_number', models.IntegerField()),
            ],
            options={
                'db_table': 'PictureWithLikesCount',
                'managed': False,
            },
        ),
    ]