# Generated by Django 4.2.5 on 2024-01-10 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m183', '0002_loginattempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginattempt',
            name='user',
        ),
        migrations.AddField(
            model_name='loginattempt',
            name='username',
            field=models.CharField(default='ads', max_length=200),
            preserve_default=False,
        ),
    ]
