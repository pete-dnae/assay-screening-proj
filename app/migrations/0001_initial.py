# Generated by Django 2.0 on 2017-12-18 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Primer',
            fields=[
                ('string_code', models.CharField(max_length=40, primary_key=True, serialize=False, unique=True)),
                ('direction', models.CharField(choices=[('FWD', 'Forward'), ('REV', 'Reverse')], max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='PrimerPair',
            fields=[
                ('string_code', models.CharField(editable=False, max_length=80, primary_key=True, serialize=False, unique=True)),
                ('role', models.CharField(choices=[('PA', 'Pre-Amp'), ('ID', 'Identification')], max_length=2)),
                ('fwd_primer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pair_fwd', to='app.Primer')),
                ('rev_primer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pair_rev', to='app.Primer')),
            ],
        ),
    ]
