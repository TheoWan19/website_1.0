from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User, Customer, Employee
from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.widgets import PhoneNumberPrefixWidget

User = get_user_model()

class DateInput(forms.DateInput):
	input_type = 'date'


class CustomerSignUpForm(UserCreationForm):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)
	
	email = forms.EmailField(
		max_length=100,
	    required=True, 
	    help_text='Enter Email Address', 
	    widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
	    )

	first_name = forms.CharField(
		max_length=100,
		required=True,
		help_text='Enter First Name',
		widget=formsTextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
		)

	last_name = forms.CharField(
		max_length=100,
		required=True,
		help_text='Enter Last Name',
		widget=formsTextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
		)

	gender = forms.ChoiceField(choices=GENDER_CHOICES)

	birth_date = forms.DateField(widget=DateInput)

	password1 = forms.CharField(
			help_text='Enter Password',
			required=True,
			widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
			)

	password2 = forms.CharField(
			help_text='Enter Password Again',
			required=True,
			widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
			)

	check = forms.BooleanField(required=True)

	class Meta(UserCreationForm.Meta):
		model = User

		widgets = {
			'mobile': PhoneNumberPrefixWidget(initial='US'),
		}

		fields = ['email', 'first_name', 'last_name', 'mobile', 'gender', 'birth_date', 'password1', 'password2', 'check']

	@transaction.atomic
	def save(self, commit=True):
		user = super().save(commit=False)
		user.is_customer = True
		if commit:
			user.save()
		customer = Customer.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), mobile=self.cleaned_data.get('mobile'), gender=self.cleaned_data.get('gender'), birth_date=self.cleaned_data.get('birth_date'))
		return user	

class LoginForm(AuthenticationForm):
	email = forms.EmailField(widget=forms)
	
