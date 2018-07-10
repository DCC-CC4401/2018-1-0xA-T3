from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_auth_login, \
	logout as django_auth_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .forms import LoginForm, RegisterForm, SearchForm, CreateArticleForm, \
	AskArticleLoanForm, ModifyArticleForm
from .models import Article, ArticleLoan, PlaceReservation
from .models import Article, ArticleLoan, PlaceReservation, User, Place
from .db_utils import any_article_id, get_article_by_id

from django.shortcuts import render

from .states import *
import re
import random
import datetime


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

def deletearticle(request, Article_id):

    if (request.method == 'POST'):
        malditoitem = Article.objects.get(pk = Article_id )
        malditoitem.delete()
        return HttpResponseRedirect('/landing-page-admin/articuloespacio')
    else:
        return render(request, '/landing_page_admin/articuloespacio.html')

def deletespace(request, Space_id):

	if (request.method == 'POST'):
		malditoitem = Place.objects.get(pk=Space_id)
		malditoitem.delete()
		return HttpResponseRedirect('/landing-page-admin/articuloespacio')
	else:
		return render(request, '/landing_page_admin/articuloespacio.html')

month_dict = {
	'Ene': 1,
	'Feb': 2,
	'Mar': 3,
	'Abr': 4,
	'May': 5,
	'Jun': 6,
	'Jul': 7,
	'Ago': 8,
	'Sep': 9,
	'Oct': 10,
	'Nov': 11,
	'Dic': 12,
}

def extract_client_date(cdate):
	regex = r'(\d{2})-(\w+)-(\d{4}), (\d{2}):(\d{2})'
	matched = re.search(regex, cdate)
	if matched is not None:
		day, month, year, hour, mins = int(matched.group(1)),\
									   int(month_dict[matched.group(2)]),\
									   int(matched.group(3)),\
									   int(matched.group(4)),\
									   int(matched.group(5))
		return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=mins)
	return None

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
	f_art_modified = False
	if request.method == 'POST':
		if 'f-art-modify-form-submit' in request.POST:
			error_msg = modify_fart(request, article)
			f_art_modified = len(error_msg) == 0
		elif 'f-art-pedir' in request.POST:
			error_msg = ask_article_loan(request, article_id)
			article_loan_requested = len(error_msg) == 0

	articles_loans = ArticleLoan.objects.filter(article=article).order_by('-id')
	date_loans = [(article_loan.init_date, article_loan.end_date) for article_loan in articles_loans]

	article_form = None
	is_admin = request.user.is_admin
	if is_admin:
		article_form = CreateArticleForm(
			initial={
				'name': article.name,
				'desc': article.desc,
				'image': article.image
			})

	context = {
		'article': article,
		'article_state': str(ArticleStates(article.state)),
		'article_state_css': ArticleStates(article.state).get_css_name(),
		'form': AskArticleLoanForm(),
		'error_msg': error_msg,
		'article_loan_requested': article_loan_requested,
		'f_art_modified': f_art_modified,
		'date_loans': date_loans,
		'is_admin': is_admin,
		'article_form': article_form
	}
	context = {**context, **common_context_logged(request)}

	return HttpResponse(template.render(context, request))


@login_required
def landing_page_admin(request):
	return HttpResponseRedirect('/landing-page-admin/usuarios')


@login_required
def landing_page_admin_usuarios(request):
	template = loader.get_template('landing_page_admin/usuarios.html')

	all_Users = User.objects.all()
	context = {
        'all_Users': all_Users
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))


@login_required
def landing_page_admin_articuloespacio(request):
	template = loader.get_template('landing_page_admin/articuloespacio.html')
	all_Articulos = Article.objects.all()
	all_Espacios = Place.objects.all()

	context = {
		'all_Articulos' : all_Articulos,
		'all_Espacios'  : all_Espacios
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))



@login_required
def landing_page_admin_grilla(request):
	template = loader.get_template('landing_page_admin/grilla.html')
	all_Reservas = PlaceReservation.objects.all().filter(state=1)
	all_Prestamos = ArticleLoan.objects.all()
	context = {
	'all_Reservas'  : all_Reservas,
	'all_Prestamos' : all_Prestamos,
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def landing_page_admin_grillav(request):
	template = loader.get_template('landing_page_admin/grilla.html')
	all_Reservas = PlaceReservation.objects.all().filter(state=1)
	all_Prestamos = ArticleLoan.objects.all().filter(state=2)
	context = {
	'all_Reservas'  : all_Reservas,
	'all_Prestamos' : all_Prestamos,
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def landing_page_admin_grillac(request):
	template = loader.get_template('landing_page_admin/grilla.html')
	all_Reservas = PlaceReservation.objects.all().filter(state=1)
	all_Prestamos = ArticleLoan.objects.all().filter(state=4)
	context = {
	'all_Reservas'  : all_Reservas,
	'all_Prestamos' : all_Prestamos,
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

@login_required
def landing_page_admin_grillap(request):
	template = loader.get_template('landing_page_admin/grilla.html')
	all_Reservas = PlaceReservation.objects.all().filter(state=1)
	all_Prestamos = ArticleLoan.objects.all().filter(state=6)
	context = {
	'all_Reservas'  : all_Reservas,
	'all_Prestamos' : all_Prestamos,
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))

def modificarPendientes(request):

	if 'aceptar' in request.POST:
		lista = request.POST.getlist('prestamos')
		for i in lista:
			prestamo = ArticleLoan.objects.get(pk= i)
			prestamo.state = 2
			prestamo.save()

		return HttpResponseRedirect('/landing-page-admin/grilla')

	elif 'rechazar' in request.POST:
		lista = request.POST.getlist('prestamos')
		for i in lista:
			prestamo = ArticleLoan.objects.get(pk=i)
			prestamo.state = 3
			prestamo.save()

		return HttpResponseRedirect('/landing-page-admin/grilla')

	elif 'obsequiar' in request.POST:
		lista = request.POST.getlist('reservas')
		for i in lista:
			reserva = PlaceReservation.objects.get(pk=i)
			reserva.state = 2
			reserva.save()

		return HttpResponseRedirect('/landing-page-admin/grilla')

	elif 'anular' in request.POST:
		lista = request.POST.getlist('reservas')
		for i in lista:
			reserva = PlaceReservation.objects.get(pk=i)
			reserva.state = 3
			reserva.save()

		return HttpResponseRedirect('/landing-page-admin/grilla')

	else:

		return render(request, '/landing_page_admin/grilla')


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

					# Checkea que el estado del articulo sea correcto
					if form.cleaned_data['state'] != 'none' \
							and item.state != \
							int(form.cleaned_data['state']):
						continue

					# Checkea que el tipo del articulo sea correcto
					if form.cleaned_data['type'] != 'none' and item.type != \
							form.cleaned_data['type']:
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

	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		ArticleLoan.objects.filter(user=request.user, id__in=todel).delete()

	context = {
		'article_history': article_history,
		'place_history': place_history
	}
	context = {**context, **common_context_logged(request)}
	return HttpResponse(template.render(context, request))


@login_required
def perfil_usuario_dueno_espacios(request):
	if request.method == 'POST':
		todel = request.POST.getlist('todelete')
		PlaceReservation.objects.filter(user=request.user,
		                                id__in=todel).delete()
	return redirect('/perfil-usuario-dueno/')


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
		init_date = str(extract_client_date(request.POST.get('init_date')))
		end_date = str(extract_client_date(request.POST.get('end_date')))
		request.POST = request.POST.copy()
		request.POST.update({
			'init_date': init_date,
			'end_date': end_date,
		})
		form = AskArticleLoanForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.article = get_article_by_id(article_id)
			post.user = request.user
			post.save()
		else:
			error_msg = form.errors

	return error_msg


def modify_fart(request, article):
	error_msg = ''
	form = ModifyArticleForm(request.POST, request.FILES)
	if form.is_valid():
		new_name = form.cleaned_data['name']
		new_desc = form.cleaned_data['desc']
		new_image = form.cleaned_data['image']
		if new_name and len(new_name) > 0:
			article.name = new_name
		if new_desc and len(new_desc) > 0:
			article.desc = new_desc
		article.save()
		if new_image:
			print("nes image!!!")
			article.image = new_image
		else:
			print("no nses image!")
		article.save()
	else:
		error_msg = form.errors

	return error_msg
