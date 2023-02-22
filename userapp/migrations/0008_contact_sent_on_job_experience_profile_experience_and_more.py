# Generated by Django 4.1.6 on 2023-02-16 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0007_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='sent_on',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='experience',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='joined_on',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='updated_on',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='modified_on',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='posted_on',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fee',
            field=models.PositiveIntegerField(blank=True, default=False, null=True),
        ),
    ]
