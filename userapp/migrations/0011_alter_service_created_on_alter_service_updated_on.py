# Generated by Django 4.1.6 on 2023-02-24 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0010_alter_skill_created_on_alter_skill_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
    ]