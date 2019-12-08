# Generated by Django 2.2.6 on 2019-12-08 07:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sublet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='id',
        ),
        migrations.AddField(
            model_name='listing',
            name='list_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bathrooms',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bedrooms',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sublet.CASUser'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='storage_size',
            field=models.PositiveIntegerField(default=0),
        ),
    ]