# Generated by Django 4.2 on 2024-06-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin_user', '0002_adminuserlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuserlist',
            name='org_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]