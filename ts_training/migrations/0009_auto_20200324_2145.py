# Generated by Django 3.0.4 on 2020-03-24 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ts_training', '0008_auto_20200324_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planned_session',
            name='slots',
            field=models.IntegerField(default=0, verbose_name='Available Slots'),
        ),
        migrations.AlterField(
            model_name='planned_session',
            name='trainingId',
            field=models.ManyToManyField(to='ts_training.Training_spec'),
        ),
        migrations.AlterField(
            model_name='training_session',
            name='trainingId',
            field=models.ManyToManyField(to='ts_training.Training_spec'),
        ),
        migrations.AlterField(
            model_name='training_spec',
            name='category',
            field=models.ForeignKey(limit_choices_to={'itemType': 'CAT'}, on_delete=django.db.models.deletion.CASCADE, to='ts_training.Icon'),
        ),
    ]
