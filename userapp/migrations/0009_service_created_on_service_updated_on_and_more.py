# Generated by Django 4.1.6 on 2023-02-24 09:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0008_contact_sent_on_job_experience_profile_experience_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='skill',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='skill',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
