# Generated by Django 2.0 on 2018-03-28 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='ReagentCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReagentGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=40)),
                ('concentration', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ReagentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.ReagentCategoryModel')),
            ],
        ),
        migrations.CreateModel(
            name='RulesScriptModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UnitsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbrev', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='reagentgroupmodel',
            name='reagent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.ReagentModel'),
        ),
        migrations.AddField(
            model_name='reagentgroupmodel',
            name='units',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.UnitsModel'),
        ),
        migrations.AddField(
            model_name='experimentmodel',
            name='rules_script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experiment_rule_script', to='app.RulesScriptModel'),
        ),
    ]
