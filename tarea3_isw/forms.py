from django import forms
from django.contrib.auth.forms import UserCreationForm

from tarea3_isw.models import Article, Types, User, ArticleLoan


class LoginForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)


class RegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	rut = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'rut', 'password1', 'password2')


class CreateArticleForm(forms.Form):
	name = forms.CharField(required=True)
	desc = forms.CharField()
	image = forms.ImageField()


class AskArticleLoanForm(forms.Form):
	init_date = forms.DateTimeField(required=True)
	end_date = forms.DateTimeField(required=True)


class SearchForm(forms.Form):
	name = forms.CharField(required=True)
	type = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxInput, queryset=Types.objects.all().values('type'))
	state = forms.MultipleChoiceField(required=False, widget=forms.CheckboxInput, choices=("Disponible", "Prestado", "En reparación", "Perdido"))
