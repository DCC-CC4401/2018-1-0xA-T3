from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as django_auth_login, logout as django_auth_logout

from django.contrib.auth.decorators import login_required

from .forms import LoginForm

@login_required
def common_context_logged(request):
	current_user = request.user
	context = {
		'current_user': current_user
	}

	return context

@login_required
def index(request):
	template = loader.get_template('base.html')
	context = {
		'nothing': 0
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def ficha_articulo(request):
	template = loader.get_template('ficha_articulo.html')
	context = {
		'nothing': 0
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def landing_page_admin(request):
	template = loader.get_template('landing_page_admin.html')
	context = {
		'nothing': 0
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def landing_page_pn(request):
	template = loader.get_template('landing_page_pn.html')
	context = {
		'nothing': 0
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def perfil_usuario_dueno(request):
	template = loader.get_template('perfil_usuario_dueno.html')
	context = {
		'nothing': 0
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
