# Generated by Django 4.0.4 on 2022-05-24 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_usercomplex_residencia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercomplex',
            name='tipoUsuario',
        ),
        migrations.AlterField(
            model_name='usercomplex',
            name='QR',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='usercomplex',
            name='correo',
            field=models.EmailField(blank=True, max_length=50),
        ),
    ]
