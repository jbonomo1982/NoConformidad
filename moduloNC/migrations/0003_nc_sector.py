# Generated by Django 2.0.9 on 2019-04-20 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moduloNC', '0002_sector'),
    ]

    operations = [
        migrations.AddField(
            model_name='nc',
            name='sector',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='moduloNC.Sector'),
        ),
    ]
