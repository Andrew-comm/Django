# Generated by Django 4.1.2 on 2022-10-08 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
