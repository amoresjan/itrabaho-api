# Generated by Django 3.2.7 on 2021-09-08 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itrabaho', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]