from abc import abstractmethod

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
	name = models.CharField(max_length=255)
	id = models.CharField(max_length=32)
	desc = models.CharField(max_length=1024)
	photo = models.ImageField()
	state = models.ExpressionList("Disponible", "Prestado", "En reparación", "Perdido")


class Espacios(models.Model):
	name = models.CharField(max_length=255)
	id = models.CharField(max_length=32)
	desc = models.CharField(max_length=1024)
	photo = models.ImageField()
	state = models.ExpressionList("Disponible", "Prestado", "En reparación")


class Prestamo(models.Model):
	article = Article()
	init_date = models.DateTimeField()
	end_date = models.DateTimeField()


class General_User(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = None

	def set_username(self, username):
		self.user.username = username

	def set_email(self, email):
		self.user.email = email

	def set_password(self, password):
		self.user.password = password


class NP_User(metaclass=General_User):
	user = User.objects.create_user()


class Admin(metaclass=General_User):
	user = User.objects.create_superuser()