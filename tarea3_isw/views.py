from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_auth_login, \
	logout as django_auth_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm, SearchForm, CreateArticleForm, \
	AskArticleLoanForm
from .models import Article, ArticleLoan, PlaceReservation
from .db_utils import any_article_id, get_article_by_id

from .states import *
import re
import random


@login_required
def common_context_logged(request):
	current_user = request.user
	context = {
		'current_user': current_user,
		'rut': current_user.rut,
		'user_enabled_class': 'dot-green' if current_user.is_enabled else 'dot-red',
		'random_val': str(random.random())
	}

	return context


@login_required
def index(request):
	return landing_page_pn(request)


def dyn_styles(request):
	template = loader.get_template('css/dynamic.css')
	context = {
		'ArticleStates_AVAILABLE': ArticleStates.AVAILABLE.get_css_name(),
		'ArticleStates_BORROWED': ArticleStates.BORROWED.get_css_name(),
		'ArticleStates_REPAIRING': ArticleStates.REPAIRING.get_css_name(),
		'ArticleStates_LOST': ArticleStates.LOST.get_css_name()
	}

	return HttpResponse(template.render(context, request))


def urlify_name(name):
	return re.sub(r'\s+', '-', name).lower()


def urlify_article_id(id):
	return '/ficha-articulo/id_%s' % str(id)


@login_required
def ficha_articulo(request, article_name, article_id):
	print("Article name:  ", article_name, " -- Article Id:  ", article_id)

	def invalid_page():
		return index(request)

	if article_id is None:
		return invalid_page()

	template = loader.get_template('ficha_articulo.html')

	article = get_article_by_id(article_id)

	if article is None:
		print("Article not found")
		return invalid_page()

	url_article_name = urlify_name(article.name)

	if article_name is None or url_article_name != article_name:
		print("redirecting!!!")
		return redirect(
			'/ficha-articulo/%s/id_%s' % (url_article_name, article_id))

	error_msg = ''
	article_loan_requested = False
	if request.method == 'POST':
		error_msg = ask_article_loan(request, article_id)
		article_loan_requested = len(error_msg) == 0


	context = {
		'article': article,
		'article_state': str(ArticleStates(article.state)),
		'article_state_css': ArticleStates(article.state).get_css_name(),
		'form': AskArticleLoanForm(),
		'error_msg': error_msg,
		'article_loan_requested': article_loan_requested
	}
	context = {**context, **common_context_logged(request)}

	return HttpResponse(template.render(context, request))


@login_required
def landing_page_admin(request):
	return HttpResponseRedirect('/landing-page-admin/usuarios')


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
		'class_espacios': '',
		'form': SearchForm(),
		'after_query': False,  # Para saber cuando ya se hizo una consulta
	}

	query = []
	n = 0
	set = []

	articles = []

	# Maneja las request de busqueda
	if request.method == 'POST':
		form = SearchForm(request.POST)

		# Articulos se agrupan de a 5 para facilitar el orden en el html

		if form.is_valid():
			try:
				for item in Article.objects.filter(
						name__icontains=form.cleaned_data['name']):
					if n == 5:
						query.append(set)
						set = []
						n = 0

					# Checkea que el tipo del articulo sea correcto
					if form.cleaned_data['type'] != 'none' and item.type != \
							form.cleaned_data['type']:
						continue

					# Checkea que el estado del articulo sea correcto
					if form.cleaned_data['state'] != 'none' and item.state != \
							form.cleaned_data['state']:
						continue

					set.append(item)
					n += 1

				# Se agregan los items que sobren, si no llegan a 5
				if n != 0:
					query.append(set)

				context['after_query'] = True

			except ValueError:
				# No items found
				pass

	else:
		for item in Article.objects.all():
			set.append(item)
			n += 1
			if n == 5:
				query.append(set)
				n = 0
				set = []

		if n != 0:
			query.append(set)

	context['query'] = query

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
	article_history = ArticleLoan.objects.filter(user=request.user) \
		                  .order_by('-init_date')[:10]

	place_history = PlaceReservation.objects.filter(user=request.user) \
		                .order_by('-init_date')[:10]

	context = {
		'article_history': article_history,
		'place_history': place_history
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
def create_article(request):
	if request.method == 'POST':
		form = CreateArticleForm(request.POST, request.FILES)
		if form.is_valid():
			article = Article()
			article.name = form.cleaned_data['name']
			article.desc = form.cleaned_data['desc']
			article.save()
			article.image = form.cleaned_data['image']
			article.save()
		else:
			print("Form is not valid")
			print(form.errors)

		return redirect('/create-article/')

	template = loader.get_template('create_article.html')
	context = {
		'form': CreateArticleForm()
	}
	context = {**context, **common_context_logged(request)}

	return HttpResponse(template.render(context, request))


def ask_article_loan(request, article_id):
	error_msg = ''
	if request.method == 'POST':
		form = AskArticleLoanForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.article = get_article_by_id(article_id)
			post.user = request.user
			post.save()
		else:
			error_msg = form.errors

	return error_msg
