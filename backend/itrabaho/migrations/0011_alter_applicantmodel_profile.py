# Generated by Django 3.2.7 on 2021-10-17 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itrabaho', '0010_auto_20211017_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantmodel',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='itrabaho.profilemodel'),
        ),
    ]