from django import forms
from django.contrib.auth.forms import UserCreationForm

from tarea3_isw.models import Article, Types, User, ArticleLoan


class LoginForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs\
			.update({'placeholder': 'e-mail'})

		self.fields['password'].widget.attrs\
			.update({'placeholder': 'password'})


class RegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	rut = forms.CharField(required=True)

	class Meta:
		model = User
		fields = (
			'email', 'first_name', 'last_name', 'rut', 'password1', 'password2')


class CreateArticleForm(forms.Form):
	name = forms.CharField(required=True)
	desc = forms.CharField()
	image = forms.ImageField()


class SearchForm(forms.Form):
	name = forms.CharField(required=True)
	type = forms.CharField(widget=forms.Select(
	                       choices=[("none", "Tipo"),
	                             ("Disponible", "Disponible"),
	                             ("Prestado", "Prestado"),
	                             ("En Reparación", "En Reparación"),
	                             ("Perdido", "Perdido")]), label="Estado")
	state = forms.CharField(widget=forms.Select(choices=[("none", "Estado")]),
	                        label="Tipo")

	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs\
			.update({'id': 'searchbar',
		             'class': 'search-bar-container-input',
		             'type': 'text',
		             'placeholder': 'Búesqueda...'})


class AskArticleLoanForm(forms.Form):
	init_date = forms.DateTimeField(required=True)
	end_date = forms.DateTimeField(required=True)

