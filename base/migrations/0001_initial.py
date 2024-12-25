# Generated by Django 5.1.3 on 2024-12-07 18:15

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('address', models.CharField(max_length=255)),
                ('education_level', models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary School'), ('university', 'University')], max_length=50)),
                ('teaching_method', models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], max_length=50)),
                ('currently_in_school', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=50)),
                ('secret_code', models.CharField(blank=True, max_length=5, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='base.courses')),
            ],
        ),
    ]
