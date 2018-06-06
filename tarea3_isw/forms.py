from django import forms
from django.contrib.auth.forms import UserCreationForm
from tarea3_isw.models import Article, Types, User


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


class SearchForm(forms.Form):
	name = forms.CharField(required=True)
	type = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxInput, queryset=Types.objects.all().values('type'))
	state = forms.MultipleChoiceField(required=False, widget=forms.CheckboxInput, choices=("Disponible", "Prestado", "En reparación", "Perdido"))

	def getResults(self):
		query = []
		n = 0
		set = []
		for item in Article.objects.filter(name__unaccent__lower__trigram_similar=self.name):
			if n == 5:
				query.append(set)
				set = []
				n = 0

			if self.type != 'none':
				if item.type != self.type:
					continue

			if self.state != 'none':
				if item.state != self.state:
					continue

			set.append(item)

		return query
