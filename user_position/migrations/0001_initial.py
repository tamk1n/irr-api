# Generated by Django 5.0.6 on 2024-05-11 13:31

from django.db import migrations, models


class Migration(migrations.Migration):
    def insert_data(apps, schema_editor):
        position = apps.get_model('user_position', 'UserPosition')
        position.objects.bulk_create([
            position(name="manager"),
            position(name="employee"),
        ])

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RunPython(insert_data),
    ]
