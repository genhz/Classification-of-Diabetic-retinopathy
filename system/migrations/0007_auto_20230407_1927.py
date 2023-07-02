# Generated by Django 3.2 on 2023-04-07 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_dr'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='doc_img',
            field=models.TextField(default='暂无'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='ranks',
            field=models.CharField(default='医师', max_length=20),
        ),
        migrations.AddField(
            model_name='doctor',
            name='subject',
            field=models.CharField(default='视网膜病变', max_length=20),
        ),
    ]