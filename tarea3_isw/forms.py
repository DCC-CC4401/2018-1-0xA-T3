from django import forms
from tarea3_isw.models import Article

class LoginForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)


class RegisterForm(forms.Form):
	name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	rut = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')

		if password != confirm_password:
			raise forms.ValidationError('password and confirm-password does not match')


class SearchForm(forms.Form):
	name = forms.CharField(required=True)
	type = forms.CharField()
	state = forms.CharField()

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