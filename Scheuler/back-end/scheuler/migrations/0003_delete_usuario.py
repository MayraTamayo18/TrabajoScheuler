# Generated by Django 4.2.15 on 2024-08-29 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheuler', '0002_remove_usuario_nombre_iniciosesion_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
