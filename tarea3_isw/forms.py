from django import forms
from django.contrib.auth.forms import UserCreationForm

from tarea3_isw.models import Article, Types, User, ArticleLoan
import datetime


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

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs\
			.update({'placeholder': 'Correo'})

		self.fields['first_name'].widget.attrs\
			.update({'placeholder': 'Nombre'})

		self.fields['last_name'].widget.attrs\
			.update({'placeholder': 'Apellido'})

		self.fields['rut'].widget.attrs\
			.update({'placeholder': 'Rut'})

		self.fields['password1'].widget.attrs\
			.update({'placeholder': 'Contraseña'})

		self.fields['password2'].widget.attrs\
			.update({'placeholder': 'Confirmar Contraseña'})

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
	                       choices=[("none", "Estado"),
	                             ("Disponible", "Disponible"),
	                             ("Prestado", "Prestado"),
	                             ("En Reparación", "En Reparación"),
	                             ("Perdido", "Perdido")]), label="Estado")
	state = forms.CharField(widget=forms.Select(choices=[("none", "Tipo")]),
	                        label="Tipo")

	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs\
			.update({'id': 'searchbar',
		             'class': 'search-bar-container-input',
		             'type': 'text',
		             'placeholder': 'Búsqueda...'})


SELECCIONAR_FECHA = 'Seleccione Fecha'

class AskArticleLoanForm(forms.ModelForm):
	class Meta:
		model = ArticleLoan
		fields = ['init_date', 'end_date']
		exclude = ['article', 'user']

		widgets = {
			'init_date': forms.TextInput(attrs={
				'class': 'ask-art-date',
				'placeholder': SELECCIONAR_FECHA
			}),
			'end_date': forms.TextInput(attrs={
				'class': 'ask-art-date',
				'placeholder': SELECCIONAR_FECHA,
			})
		}
		labels = {
			'init_date': 'Desde',
			'end_date':  'Hasta'
		}

	def clean(self):
		data = self.cleaned_data
		if data['init_date'] > data['end_date']:
			raise forms.ValidationError(u'La fecha de inicio debe ser antes de la fecha de término')

		next_hour = datetime.datetime.now() + datetime.timedelta(hours=1)

		if data['init_date'].date() < next_hour.date() :
			raise forms.ValidationError(u'La fecha de inicio debe ser al menos en una hora')