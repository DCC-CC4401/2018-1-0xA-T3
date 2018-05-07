from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.


def index(request):
	template = loader.get_template('base/index.html')
	context = {
		'nothing': 0
	}
	return HttpResponse(template.render(context, request))


def ficha_articulo(request):
	template = loader.get_template('ficha_articulo/ficha_articulo.html')
	context = {
		'nothing': 0
	}
	return HttpResponse(template.render(context, request))

def landing_page_admin(request):
	template = loader.get_template('landing_page_admin/landing_page_admin.html')
	context = {
		'nothing': 0
	}
	return HttpResponse(template.render(context, request))


def landing_page_pn(request):
	template = loader.get_template('landing_page_pn/landing_page_pn.html')
	context = {
		'nothing': 0
	}
	return HttpResponse(template.render(context, request))


def perfil_usuario_dueno(request):
	template = loader.get_template('perfil_usuario_dueno/perfil_usuario_dueno.html')
	context = {
		'nothing': 0
	}
	return HttpResponse(template.render(context, request))
