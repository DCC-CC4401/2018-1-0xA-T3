from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
# Create your models here.


class Article(models.Model):
	name = models.CharField(max_length=255)
	id = models.CharField(max_length=32, primary_key=True)
	desc = models.CharField(max_length=1024)
	photo = models.ImageField()
	state = models.ExpressionList("Disponible", "Prestado", "En reparación", "Perdido")


class Espacio(models.Model):
	name = models.CharField(max_length=255)
	id = models.CharField(max_length=32, primary_key=True)
	desc = models.CharField(max_length=1024)
	photo = models.ImageField()
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


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	rut = models.CharField(max_length=15)
	enabled = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()




# to authenticate with mail
class EmailBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		user_model = get_user_model()
		try:
			print("authenticating.. ")
			print("username: ", username)
			print("password: ", password)
			print("email: ", kwargs.get('email'))
			user = user_model.objects.get(email=kwargs.get('email'))
		except user_model.DoesNotExist:
			return None
		else:
			if user.check_password(password):
				return user
		return None

