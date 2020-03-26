# Generated by Django 3.0.4 on 2020-03-25 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ts_training', '0010_auto_20200325_1450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planned_session',
            old_name='trainee',
            new_name='signed_up',
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
    ]