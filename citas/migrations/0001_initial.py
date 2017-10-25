# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 03:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('fecha', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('ausente', models.BooleanField(default=False)),
                ('atendida', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Consultorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('especialista', models.BooleanField(default=False)),
                ('horario_inicio', models.TimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('horario_fin', models.TimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('administradores', models.ManyToManyField(blank=True, related_name='consultorios_administrados', to=settings.AUTH_USER_MODEL)),
                ('secretaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secretarias', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultorios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['nombre'],
                'permissions': (('consultorio', 'Permite al usuario gestionar consultorios'), ('clinical_read', 'Permite que el usuario tenga acceso a los datos cl\xednicos'), ('clinical_write', 'Permite que el usuario escriba a los datos cl\xednicos'), ('clinical_manage', 'Permite que el usuario escriba a los datos cl\xednicos')),
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id_persona', models.IntegerField()),
                ('nombre_completo', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cita',
            name='consultorio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='citas.Consultorio'),
        ),
        migrations.AddField(
            model_name='cita',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='citas.Persona'),
        ),
    ]
