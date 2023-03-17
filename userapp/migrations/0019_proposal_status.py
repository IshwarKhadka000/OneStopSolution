# Generated by Django 4.1.6 on 2023-03-13 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0018_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='status',
            field=models.CharField(choices=[('applied', 'applied'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='applied', max_length=20),
        ),
    ]
