# Generated by Django 4.1.6 on 2023-02-15 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_job_postedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='applied_by',
            field=models.ManyToManyField(blank=True, null=True, to='userapp.profile'),
        ),
    ]