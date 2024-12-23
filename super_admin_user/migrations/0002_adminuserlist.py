# Generated by Django 4.2 on 2024-06-22 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('super_admin_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUserList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('address', models.TextField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('superadmin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='superadmins', to='super_admin_user.superadmin')),
            ],
        ),
    ]
