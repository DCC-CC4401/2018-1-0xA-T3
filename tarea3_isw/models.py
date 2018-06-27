from django.db import models

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager
# Create your models here.


class Article(models.Model):
	name = models.CharField(max_length=255)
	id = models.CharField(max_length=32, primary_key=True)
	desc = models.CharField(max_length=1024)
	#photo = models.ImageField()
	state = models.ExpressionList("Disponible", "Prestado", "En reparación", "Perdido")
	type = models.CharField(max_length=32)


class Espacio(models.Model):
	name = models.CharField(max_length=255)
	id = models.CharField(max_length=32, primary_key=True)
	desc = models.CharField(max_length=1024)
	#photo = models.ImageField()
	state = models.ExpressionList("Disponible", "Prestado", "En reparación")


class Prestamo(models.Model):
	article = Article()
	init_date = models.DateTimeField()
	end_date = models.DateTimeField()
	state = models.ExpressionList("En proceso", "Aprobado", "Rechazado", "Caducado", "Finalizado")


class Reserva(models.Model):
	espacio = Espacio()
	init_date = models.DateTimeField()
	end_date = models.DateTimeField()
	state = models.ExpressionList("En proceso", "Aprobada", "Rechazada", "Finalizada")


class Types(models.Model):
	type = models.CharField(max_length=32, primary_key=True, default='none')


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField('Correo electronico', unique=True)
	first_name = models.CharField('Primer nombre', max_length=30, blank=True)
	last_name = models.CharField('Apellido', max_length=30, blank=True)
	rut = models.CharField('Rut', max_length=15, unique=True)
	date_joined = models.DateTimeField('Fecha de registro', auto_now_add=True)
	is_active = models.BooleanField('Activo', default=True)
	is_enabled = models.BooleanField('Habilitado', default=True)

	is_admin = models.BooleanField('Es admin', default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'rut']

	class Meta:
		verbose_name = 'usuario'
		verbose_name_plural = 'usuarios'

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)