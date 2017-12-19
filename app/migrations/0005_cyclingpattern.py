# Generated by Django 2.0 on 2017-12-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_strain'),
    ]

    operations = [
        migrations.CreateModel(
            name='CyclingPattern',
            fields=[
                ('pattern_name', models.CharField(max_length=80, primary_key=True, serialize=False, unique=True)),
                ('activation_time', models.PositiveIntegerField()),
                ('activation_temp', models.PositiveIntegerField()),
                ('num_cycles', models.PositiveIntegerField()),
                ('denature_temp', models.PositiveIntegerField()),
                ('denature_time', models.PositiveIntegerField()),
                ('anneal_temp', models.PositiveIntegerField()),
                ('anneal_time', models.PositiveIntegerField()),
                ('extend_temp', models.PositiveIntegerField()),
                ('extend_time', models.PositiveIntegerField()),
            ],
        ),
    ]
