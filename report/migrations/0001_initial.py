# Generated by Django 5.0.6 on 2024-05-17 09:04

import django.db.models.deletion
import report.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('division', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObservationFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObservationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObservationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InspectionReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('project', models.TextField()),
                ('responsible_person', models.CharField(max_length=155)),
                ('issue_date', models.DateField(auto_now=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='division.division')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='division.divisionfield')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReportObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('reference_doc', models.CharField(max_length=155)),
                ('action', models.TextField()),
                ('deadline', models.DateField()),
                ('close_date', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='report.observationcategory')),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='report.observationfactor')),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to=settings.AUTH_USER_MODEL)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='report.inspectionreport')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='report.observationstatus')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='report.observationtype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObservationEvidence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('evidence', models.ImageField(upload_to=report.models.evidences_path)),
                ('observation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidences', to='report.reportobservation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]