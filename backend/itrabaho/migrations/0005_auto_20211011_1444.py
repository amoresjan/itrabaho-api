# Generated by Django 3.2.7 on 2021-10-11 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("itrabaho", "0004_auto_20211007_0250"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reviewmodel",
            name="jobPostId",
        ),
        migrations.AddField(
            model_name="jobpostmodel",
            name="applicantId",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="itrabaho.applicantmodel",
            ),
        ),
        migrations.AddField(
            model_name="jobpostmodel",
            name="applicantReviewId",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="itrabaho.reviewmodel",
            ),
        ),
        migrations.AddField(
            model_name="jobpostmodel",
            name="recruiterReviewId",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="itrabaho.reviewmodel",
            ),
        ),
        migrations.AlterField(
            model_name="jobpostmodel",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("H", "Hiring"), ("A", "Active"), ("D", "Done")],
                default="H",
                max_length=1,
                null=True,
            ),
        ),
    ]
