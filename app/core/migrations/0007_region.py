# Generated by Django 2.1.7 on 2019-03-14 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
