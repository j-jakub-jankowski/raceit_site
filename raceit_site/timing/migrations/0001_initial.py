# Generated by Django 3.0.1 on 2020-01-21 19:17

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChronoResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
                ('chrono', models.CharField(max_length=50)),
                ('gun_time', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=50)),
                ('team', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('distance', models.FloatField()),
                ('date_and_time', models.DateTimeField(blank=True, null=True)),
                ('town', models.CharField(max_length=100)),
                ('race_info', ckeditor.fields.RichTextField(blank=True)),
                ('race_rules', ckeditor.fields.RichTextField(blank=True)),
                ('race_route', ckeditor.fields.RichTextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('bib_number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RoutePoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_name', models.CharField(max_length=10)),
                ('point_distance', models.FloatField()),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timing.Race')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=5)),
                ('gun_time', models.CharField(max_length=11)),
                ('competitor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', related_query_name='results', to='timing.Competitor')),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timing.RoutePoint')),
            ],
        ),
        migrations.AddField(
            model_name='competitor',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timing.Race'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='tag',
            field=models.OneToOneField(on_delete=models.SET(0), to='timing.Tag'),
        ),
        migrations.CreateModel(
            name='ChronoFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.PositiveSmallIntegerField(choices=[(1, 'Normal'), (2, 'Immediate')], default=1)),
                ('chrono_file_path', models.FilePathField(path='C:/Users/Pomiar czasu/Desktop/Projekty_python/timing/timing_site/chrono_files/')),
                ('reading_flag', models.BooleanField()),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timing.RoutePoint')),
            ],
        ),
    ]
