from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_auth_login, logout as django_auth_logout
from django.shortcuts import redirect


from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm, SearchForm


@login_required
def common_context_logged(request):
	current_user = request.user
	context = {
		'current_user': current_user,
		'rut': current_user.rut,
		'user_enabled_class': 'dot-green' if current_user.is_enabled else 'dot-red'
	}

	return context


@login_required
def index(request):
	return landing_page_pn(request)


@login_required
def ficha_articulo(request):
	template = loader.get_template('ficha_articulo.html')
	context = {
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))


@login_required
def landing_page_admin(request):
	template = loader.get_template('landing_page_admin.html')
	context = {
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def landing_page_admin_usuarios(request):
	template = loader.get_template('landing_page_admin/usuarios.html')
	context = {
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def landing_page_admin_articuloespacio(request):
	template = loader.get_template('landing_page_admin/articuloespacio.html')
	context = {
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def landing_page_admin_grilla(request):
	template = loader.get_template('landing_page_admin/grilla.html')
	context = {
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))


@login_required
def landing_page_pn(request):
	return HttpResponseRedirect('/landing-page-pn/articulos/')


@login_required
def landing_page_pn_articulos(request):
	template = loader.get_template('landing_page_pn/articulos.html')
	context = {
		'class_articulos': 'active',
		'class_espacios': ''
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))


@login_required
def landing_page_pn_espacios(request):
	template = loader.get_template('landing_page_pn/espacios.html')
	context = {
		'class_articulos': '',
		'class_espacios': 'active'
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))


@login_required
def perfil_usuario_dueno(request):
	template = loader.get_template('perfil_usuario_dueno.html')
	context = {
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))


def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = authenticate(email=email, password=password)
			if user is not None:
				django_auth_login(request, user)
				if user.is_admin:
					return landing_page_admin(request)
				return landing_page_pn(request)
			else:
				print("mal user")

	template = loader.get_template('login.html')
	context = {
		'form': LoginForm()
	}

	return HttpResponse(template.render(context, request))


@login_required
def logout(request):
	django_auth_logout(request)

	return login(request)


def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')

	template = loader.get_template('register.html')
	context = {
		'form': RegisterForm()
	}

	return HttpResponse(template.render(context, request))


@login_required
def article_search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			template = loader.get_template('landing_page_pn/articulos.html')
			context = {
				'query': form.getResults()
			}

			return HttpResponse(template.render(context, request))
