# Generated by Django 4.2.5 on 2024-01-10 10:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('m183', '0004_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
