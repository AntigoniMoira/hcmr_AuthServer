# Generated by Django 2.0.5 on 2018-09-30 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='permission',
            field=models.CharField(choices=[('U', 'User'), ('S', 'Staff'), ('A', 'Admin')], default='U', max_length=1),
        ),
    ]
