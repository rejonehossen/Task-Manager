# Generated by Django 5.2.3 on 2025-06-18 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(blank=True, choices=[('H', 'High 🔥'), ('M', 'Medium ⭐'), ('L', 'Low ✅')], max_length=1, null=True),
        ),
    ]
