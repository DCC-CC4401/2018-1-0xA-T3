from django.db import models

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

class Reservas(models.Model):
	article = Article()
	init_date = models.DateTimeField()
	end_date = models.DateTimeField()


