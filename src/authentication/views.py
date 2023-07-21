from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from .models import User
from .forms import CustomerSignUpForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import customer_required, employee_required
from django.contrib import messages

# Create your views here.
class CustomerSignUpView(CreateView):
	model = User
	form_class = CustomerSignUpForm
	template_name = 'authentication/customer_signup.html'

	succes_message = ''


	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'customer'
		return super().get_context_data(**kwargs)


	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		succes_message = self.get_success_message(form.cleaned_data)
		if succes_message:
			messages.success(self.request, 'Account was created for ' + user)
		return redirect('customer-home')

	def get_success_message(self, cleaned_data):
		return self.succes_message % cleaned_data



class LoginView(View):
	template_name = 'authentication/login.html'
	form_class = LoginForm

	def get(self, request):
		form = self.form_class()
		message = ''
		return render(request, self.template_name, context={'form': form, 'message': message})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = authenticate(
					username = form.cleaned_data['username'],
					password = form.cleaned_data['password'],
			)
			if user.is_customer:
				return reverse('customer-home')
			if user.is_employee:
				return reverse('employee-home')	
			if user is not None:
				login(request, user)
				message = f"Bonjour, {user.username} ! Vous êtes connecté."
				return redirect('home')	
		message = 'Identifiants invalides.'
		return render(request, self.template_name, context={'form': form, 'message': message})	
		

@login_required
@customer_required
def customer_home(request):
	return render(request, 'authentication/customer_home.html')

@login_required
@employee_required
def employee_view(request):
	pass

class EmployeeSignUpView(CreateView):
	pass			