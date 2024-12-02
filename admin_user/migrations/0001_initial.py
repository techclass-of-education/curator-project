# Generated by Django 4.2 on 2024-07-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('profileImage', models.ImageField(upload_to='profiles/')),
                ('org_id', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=255)),
                ('date_reg', models.DateField()),
            ],
        ),
    ]