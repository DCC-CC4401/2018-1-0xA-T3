# Generated by Django 2.0.7 on 2018-07-04 16:25

from django.db import migrations, models
import tarea3_isw.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo electronico')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='Primer nombre')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Apellido')),
                ('rut', models.CharField(max_length=15, unique=True, verbose_name='Rut')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('is_enabled', models.BooleanField(default=True, verbose_name='Habilitado')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Es admin')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
            },
            managers=[
                ('objects', tarea3_isw.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=1024)),
                ('type', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Espacio',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('init_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('init_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('type', models.CharField(default='none', max_length=32, primary_key=True, serialize=False)),
            ],
        ),
    ]
