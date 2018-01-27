# Generated by Django 2.0 on 2018-01-27 16:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllocationInstructions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suppressed_columns', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AllocRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_for_ordering', models.PositiveIntegerField()),
                ('payload_type', models.CharField(choices=[('Unspecified', 'Unspecified'), ('Dilution Factor', 'Dilution Factor'), ('HgDNA', 'HgDNA'), ('PA Primers', 'PA Primers'), ('ID Primers', 'ID Primers'), ('Strain', 'Strain'), ('Strain Count', 'Strain Count')], max_length=15)),
                ('payload_csv', models.CharField(max_length=500)),
                ('pattern', models.CharField(choices=[('Consecutive', 'Consecutive'), ('In Blocks', 'In Blocks')], max_length=15)),
                ('start_row_letter', models.CharField(max_length=1, validators=[django.core.validators.RegexValidator(re.compile('[A-Z]'))])),
                ('end_row_letter', models.CharField(max_length=1, validators=[django.core.validators.RegexValidator(re.compile('[A-Z]'))])),
                ('start_column', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(20)])),
                ('end_column', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(20)])),
            ],
            options={
                'ordering': ('rank_for_ordering',),
            },
        ),
        migrations.CreateModel(
            name='Arg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BufferMix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.PositiveIntegerField()),
                ('final_volume', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Concentration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.DecimalField(decimal_places=2, max_digits=8)),
                ('final', models.DecimalField(decimal_places=2, max_digits=8)),
                ('units', models.CharField(choices=[('X', 'X'), ('mM', 'mM'), ('mg/ml', 'mg/ml'), ('mM each', 'mM each'), ('microM each', 'microM each'), ('ng/ul', 'ng/ul'), ('cp/ul', 'cp/ul'), ('%', '%')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='ConcreteReagent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('lot', models.CharField(max_length=30)),
                ('concentration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reagent', to='app.Concentration')),
            ],
        ),
        migrations.CreateModel(
            name='CyclingPattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_name', models.CharField(max_length=80, unique=True)),
                ('designer_name', models.CharField(max_length=80)),
                ('id_cycling', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiment_id_cycling', to='app.CyclingPattern')),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MasterMix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_volume', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MixedReagent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buffer_mix', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mixed_reagent', to='app.BufferMix')),
                ('concentration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mixed_reagent', to='app.Concentration')),
            ],
        ),
        migrations.CreateModel(
            name='Organism',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=8, unique=True)),
                ('full_name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceholderReagent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Primers', 'Primers'), ('Template', 'Template'), ('HgDNA', 'HgDNA')], max_length=15)),
                ('concentration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='placeholder_reagent', to='app.Concentration')),
            ],
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('allocation_instructions', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='plate', to='app.AllocationInstructions')),
            ],
        ),
        migrations.CreateModel(
            name='Primer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oligo_code', models.CharField(max_length=30)),
                ('full_name', models.CharField(max_length=50, unique=True)),
                ('role', models.CharField(choices=[('fwd', 'fwd'), ('rev', 'rev')], max_length=15)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primer', to='app.Gene')),
                ('organism', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primer', to='app.Organism')),
            ],
        ),
        migrations.CreateModel(
            name='PrimerKit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fwd_concentration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primer_kit_fwd', to='app.Concentration')),
            ],
        ),
        migrations.CreateModel(
            name='PrimerPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suitable_for_pa', models.BooleanField()),
                ('suitable_for_id', models.BooleanField()),
                ('forward_primer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primer_pair_fwd', to='app.Primer')),
                ('reverse_primer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primer_pair_rev', to='app.Primer')),
            ],
            options={
                'ordering': ('forward_primer__organism__abbreviation', 'forward_primer__gene__name', 'forward_primer__full_name', 'reverse_primer__full_name'),
            },
        ),
        migrations.CreateModel(
            name='RuleList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rules', models.ManyToManyField(to='app.AllocRule')),
            ],
        ),
        migrations.CreateModel(
            name='Strain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('genome_size', models.BigIntegerField()),
                ('arg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='strain_arg', to='app.Arg')),
                ('organism', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='strain_organism', to='app.Organism')),
            ],
            options={
                'ordering': ('organism__abbreviation', 'arg__name'),
            },
        ),
        migrations.CreateModel(
            name='StrainKit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strains', models.ManyToManyField(to='app.Strain')),
            ],
        ),
        migrations.AddField(
            model_name='primerkit',
            name='id_primers',
            field=models.ManyToManyField(related_name='primer_pair_id', to='app.PrimerPair'),
        ),
        migrations.AddField(
            model_name='primerkit',
            name='pa_primers',
            field=models.ManyToManyField(related_name='primer_pair_pa', to='app.PrimerPair'),
        ),
        migrations.AddField(
            model_name='primerkit',
            name='rev_concentration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primer_kit_rev', to='app.Concentration'),
        ),
        migrations.AddField(
            model_name='mastermix',
            name='buffer_mix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='master_mix_buffermix', to='app.MixedReagent'),
        ),
        migrations.AddField(
            model_name='mastermix',
            name='hgDNA',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='master_mix_hgDNA', to='app.PlaceholderReagent'),
        ),
        migrations.AddField(
            model_name='mastermix',
            name='primers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='master_mix_primers', to='app.PlaceholderReagent'),
        ),
        migrations.AddField(
            model_name='mastermix',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='master_mix_template', to='app.PlaceholderReagent'),
        ),
        migrations.AddField(
            model_name='mastermix',
            name='water',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='master_mix_water', to='app.ConcreteReagent'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='id_mastermix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiment_id', to='app.MasterMix'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='pa_cycling',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiment_pa_cycling', to='app.CyclingPattern'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='pa_mastermix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiment_pa', to='app.MasterMix'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='plates',
            field=models.ManyToManyField(to='app.Plate'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='primer_kit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiment_primer_kit', to='app.PrimerKit'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='strain_kit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiment_strain_kit', to='app.StrainKit'),
        ),
        migrations.AddField(
            model_name='buffermix',
            name='concrete_reagents',
            field=models.ManyToManyField(to='app.ConcreteReagent'),
        ),
        migrations.AddField(
            model_name='allocationinstructions',
            name='rule_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='instructions', to='app.RuleList'),
        ),
    ]
